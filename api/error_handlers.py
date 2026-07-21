"""
Error handlers and middleware for API exception handling.

This module provides centralized error handling and custom exception handlers
for the REST API.
"""
import logging
from django.db import IntegrityError, OperationalError, DatabaseError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class APIExceptionHandler:
    """
    Centralized handler for API exceptions.
    
    This class provides methods to handle various types of exceptions and return
    appropriate HTTP responses with meaningful error messages.
    """
    
    @staticmethod
    def handle_integrity_error(exc, context):
        """
        Handle database integrity errors (unique constraint violations).
        
        Args:
            exc (IntegrityError): The integrity error exception
            context (dict): Exception context from DRF
            
        Returns:
            Response: JSON response with 400 status and error details
        """
        error_message = str(exc)
        
        # Extract field from error message
        if "email" in error_message.lower():
            detail = {
                "email": ["A customer with this email already exists."]
            }
        elif "national_id" in error_message.lower():
            detail = {
                "national_id_number": ["A customer with this national ID already exists."]
            }
        else:
            detail = {
                "detail": "A resource with these values already exists."
            }
        
        logger.warning(f"Integrity error: {error_message}")
        return Response(detail, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def handle_database_error(exc, context):
        """
        Handle general database errors.
        
        Args:
            exc (Exception): The database error exception
            context (dict): Exception context from DRF
            
        Returns:
            Response: JSON response with 503 status
        """
        logger.error(f"Database error: {str(exc)}", exc_info=True)
        return Response(
            {"detail": "Database operation failed. Please try again later."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    @staticmethod
    def handle_operational_error(exc, context):
        """
        Handle database operational errors (connection issues, server down).
        
        Args:
            exc (OperationalError): The operational error exception
            context (dict): Exception context from DRF
            
        Returns:
            Response: JSON response with 503 status
        """
        logger.error(f"Database operational error: {str(exc)}", exc_info=True)
        return Response(
            {"detail": "Database service unavailable. Please try again later."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    @staticmethod
    def handle_validation_error(exc, context):
        """
        Handle Django validation errors.
        
        Args:
            exc (ValidationError): The validation error exception
            context (dict): Exception context from DRF
            
        Returns:
            Response: JSON response with 400 status
        """
        if hasattr(exc, 'message_dict'):
            detail = exc.message_dict
        elif hasattr(exc, 'messages'):
            detail = {"detail": exc.messages}
        else:
            detail = {"detail": str(exc)}
        
        logger.warning(f"Validation error: {detail}")
        return Response(detail, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def handle_object_does_not_exist(exc, context):
        """
        Handle ObjectDoesNotExist errors.
        
        Args:
            exc (ObjectDoesNotExist): The object does not exist exception
            context (dict): Exception context from DRF
            
        Returns:
            Response: JSON response with 404 status
        """
        logger.warning(f"Object not found: {str(exc)}")
        return Response(
            {"detail": "The requested resource was not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def handle_file_error(exc, context):
        """
        Handle file operation errors.
        
        Args:
            exc (Exception): The file error exception
            context (dict): Exception context from DRF
            
        Returns:
            Response: JSON response with 500 status
        """
        error_type = type(exc).__name__
        logger.error(f"File operation error ({error_type}): {str(exc)}", exc_info=True)
        
        if "PermissionError" in error_type:
            return Response(
                {"detail": "Permission denied for file operation."},
                status=status.HTTP_403_FORBIDDEN
            )
        elif "OSError" in error_type or "IOError" in error_type:
            return Response(
                {"detail": "File storage service unavailable."},
                status=status.HTTP_507_INSUFFICIENT_STORAGE
            )
        else:
            return Response(
                {"detail": "File operation failed."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @staticmethod
    def handle_general_exception(exc, context):
        """
        Handle unexpected exceptions.
        
        Args:
            exc (Exception): The exception
            context (dict): Exception context from DRF
            
        Returns:
            Response: JSON response with 500 status
        """
        error_type = type(exc).__name__
        logger.error(
            f"Unexpected error ({error_type}): {str(exc)}",
            exc_info=True,
            extra={
                "request_method": context.get("request").method if context.get("request") else None,
                "request_path": context.get("request").path if context.get("request") else None,
            }
        )
        return Response(
            {"detail": "An unexpected error occurred. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def custom_exception_handler(exc, context):
    """
    Custom DRF exception handler with comprehensive error handling.
    
    This function handles both DRF exceptions and custom application exceptions.
    It provides appropriate HTTP status codes and user-friendly error messages.
    
    Args:
        exc (Exception): The exception that was raised
        context (dict): Dictionary containing request, view, and other context
        
    Returns:
        Response: DRF Response object with error details and appropriate status code
        
    Example:
        This should be configured in Django settings.py:
        
        REST_FRAMEWORK = {
            'EXCEPTION_HANDLER': 'api.error_handlers.custom_exception_handler'
        }
    """
    # Handle DRF exceptions first (they return a Response)
    if isinstance(exc, APIException):
        return Response(
            {"detail": str(exc.detail)},
            status=exc.status_code
        )
    
    # Handle database integrity errors (duplicate fields, constraints)
    if isinstance(exc, IntegrityError):
        return APIExceptionHandler.handle_integrity_error(exc, context)
    
    # Handle database operational errors (connection issues)
    if isinstance(exc, OperationalError):
        return APIExceptionHandler.handle_operational_error(exc, context)
    
    # Handle general database errors
    if isinstance(exc, DatabaseError):
        return APIExceptionHandler.handle_database_error(exc, context)
    
    # Handle Django validation errors
    if isinstance(exc, ValidationError):
        return APIExceptionHandler.handle_validation_error(exc, context)
    
    # Handle object not found
    if isinstance(exc, ObjectDoesNotExist):
        return APIExceptionHandler.handle_object_does_not_exist(exc, context)
    
    # Handle file operation errors
    if isinstance(exc, (FileNotFoundError, PermissionError, OSError, IOError)):
        return APIExceptionHandler.handle_file_error(exc, context)
    
    # Handle all other exceptions
    return APIExceptionHandler.handle_general_exception(exc, context)
