"""
Custom exceptions for the Customer Management API.

This module defines custom exception classes for handling application-specific errors.
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class DuplicateEmailError(APIException):
    """
    Exception raised when attempting to create a customer with a duplicate email.
    
    Attributes:
        status_code (int): HTTP 400 Bad Request
        default_detail (str): Error message
        default_code (str): Error code for identification
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A customer with this email already exists."
    default_code = "duplicate_email"


class DuplicateNationalIDError(APIException):
    """
    Exception raised when attempting to create a customer with a duplicate national ID.
    
    Attributes:
        status_code (int): HTTP 400 Bad Request
        default_detail (str): Error message
        default_code (str): Error code for identification
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A customer with this national ID number already exists."
    default_code = "duplicate_national_id"


class InvalidDateFormatError(APIException):
    """
    Exception raised when date format is invalid.
    
    Attributes:
        status_code (int): HTTP 400 Bad Request
        default_detail (str): Error message
        default_code (str): Error code for identification
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid date format. Use YYYY-MM-DD format."
    default_code = "invalid_date_format"


class FileTooLargeError(APIException):
    """
    Exception raised when uploaded file exceeds maximum size.
    
    Attributes:
        status_code (int): HTTP 413 Payload Too Large
        default_detail (str): Error message
        default_code (str): Error code for identification
    """
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    default_detail = "File size exceeds maximum allowed size (10MB)."
    default_code = "file_too_large"


class InvalidFileTypeError(APIException):
    """
    Exception raised when file type is not allowed.
    
    Attributes:
        status_code (int): HTTP 400 Bad Request
        default_detail (str): Error message
        default_code (str): Error code for identification
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "File type not allowed. Allowed types: PDF, JPG, JPEG, PNG, GIF, DOC, DOCX."
    default_code = "invalid_file_type"


class FileStorageError(APIException):
    """
    Exception raised when file storage operation fails.
    
    Attributes:
        status_code (int): HTTP 507 Insufficient Storage
        default_detail (str): Error message
        default_code (str): Error code for identification
    """
    status_code = status.HTTP_507_INSUFFICIENT_STORAGE
    default_detail = "Unable to save file. Please try again later."
    default_code = "file_storage_error"


class InvalidPaginationError(APIException):
    """
    Exception raised when pagination parameters are invalid.
    
    Attributes:
        status_code (int): HTTP 400 Bad Request
        default_detail (str): Error message
        default_code (str): Error code for identification
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid pagination parameters. Page must be a positive integer."
    default_code = "invalid_pagination"


class DatabaseError(APIException):
    """
    Exception raised when database operation fails.
    
    Attributes:
        status_code (int): HTTP 503 Service Unavailable
        default_detail (str): Error message
        default_code (str): Error code for identification
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Database operation failed. Please try again later."
    default_code = "database_error"


class InvalidInputError(APIException):
    """
    Exception raised for invalid input data.
    
    Attributes:
        status_code (int): HTTP 400 Bad Request
        default_detail (str): Error message
        default_code (str): Error code for identification
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid input data provided."
    default_code = "invalid_input"


class MissingRequiredFieldError(APIException):
    """
    Exception raised when required field is missing.
    
    Attributes:
        status_code (int): HTTP 400 Bad Request
        default_detail (str): Error message
        default_code (str): Error code for identification
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Missing required field."
    default_code = "missing_required_field"
