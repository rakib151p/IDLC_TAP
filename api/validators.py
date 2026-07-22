"""
Custom validators for API serializers.

This module provides validation functions for common data types and formats.
"""
from datetime import datetime
from django.core.exceptions import ValidationError
from api.exceptions import (
    InvalidDateFormatError,
    InvalidInputError,
    FileTooLargeError,
    InvalidFileTypeError,
)

# File upload constraints
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_EXTENSIONS = {
    'pdf', 'jpg', 'jpeg', 'png', 'gif', 'doc', 'docx', 'txt'
}
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'image/jpeg',
    'image/png',
    'image/gif',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
}


def validate_date_of_birth(value):
    """
    Validate date of birth format and ensure it's in the past.
    
    Args:
        value (date): Date of birth to validate
        
    Raises:
        InvalidDateFormatError: If date format is invalid or date is in the future
        TypeError: If value is not a date object
        
    Example:
        >>> from datetime import date
        >>> validate_date_of_birth(date(1990, 1, 1))  # Valid
        >>> validate_date_of_birth(date(2050, 1, 1))  # Raises error
    """
    try:
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d").date()
        
        today = datetime.now().date()
        if value >= today:
            raise InvalidDateFormatError(
                detail="Date of birth must be in the past."
            )
        
        # Check age is reasonable (not more than 150 years old)
        age = (today - value).days // 365
        if age > 150:
            raise InvalidDateFormatError(
                detail="Invalid date of birth. Age cannot exceed 150 years."
            )
            
    except ValueError as e:
        raise InvalidDateFormatError(
            detail="Invalid date format. Use YYYY-MM-DD format."
        )
    except TypeError as e:
        raise InvalidInputError(
            detail="Date must be provided in YYYY-MM-DD format."
        )


def validate_email(value):
    """
    Validate email format.
    
    Args:
        value (str): Email address to validate
        
    Raises:
        InvalidInputError: If email format is invalid
        
    Example:
        >>> validate_email("user@example.com")  # Valid
        >>> validate_email("invalid-email")  # Raises error
    """
    try:
        from django.core.validators import validate_email as django_validate_email
        django_validate_email(value)
    except ValidationError:
        raise InvalidInputError(
            detail="Invalid email format."
        )


def validate_national_id(value):
    """
    Validate national ID format (basic validation).
    
    Args:
        value (str): National ID number to validate
        
    Raises:
        InvalidInputError: If national ID is empty or too long
        
    Example:
        >>> validate_national_id("1234567890")  # Valid
        >>> validate_national_id("")  # Raises error
    """
    if not value or len(value) < 5:
        raise InvalidInputError(
            detail="National ID must be at least 5 characters."
        )
    
    if len(value) > 50:
        raise InvalidInputError(
            detail="National ID cannot exceed 50 characters."
        )
    
    # Remove whitespace and check if it contains only alphanumeric
    clean_id = value.strip()
    if not clean_id.replace(" ", "").isalnum():
        raise InvalidInputError(
            detail="National ID can only contain letters, numbers, and spaces."
        )


def validate_phone_number(value):
    """
    Validate phone number format.
    
    Args:
        value (str): Phone number to validate
        
    Raises:
        InvalidInputError: If phone number format is invalid
        
    Example:
        >>> validate_phone_number("+880123456789")  # Valid
        >>> validate_phone_number("123")  # Raises error
    """
    if not value:
        raise InvalidInputError(detail="Phone number cannot be empty.")
    
    # Remove common separators
    clean_number = value.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    # Must contain at least 7 digits
    digit_count = sum(1 for c in clean_number if c.isdigit())
    if digit_count < 7:
        raise InvalidInputError(
            detail="Phone number must contain at least 7 digits."
        )
    
    # Cannot exceed 20 characters
    if len(clean_number) > 20:
        raise InvalidInputError(
            detail="Phone number cannot exceed 20 characters."
        )
    
    # Must start with + or digit
    if not (clean_number[0] in ['+', '0'] or clean_number[0].isdigit()):
        raise InvalidInputError(
            detail="Phone number must start with + or a digit."
        )


def validate_postal_code(value):
    """
    Validate postal code format.
    
    Args:
        value (str): Postal code to validate
        
    Raises:
        InvalidInputError: If postal code is invalid
        
    Example:
        >>> validate_postal_code("1000")  # Valid
        >>> validate_postal_code("")  # Raises error
    """
    if not value:
        raise InvalidInputError(detail="Postal code cannot be empty.")
    
    clean_code = value.strip()
    if len(clean_code) < 3:
        raise InvalidInputError(
            detail="Postal code must be at least 3 characters."
        )
    
    if len(clean_code) > 20:
        raise InvalidInputError(
            detail="Postal code cannot exceed 20 characters."
        )


def validate_file_upload(file_obj):
    """
    Validate uploaded file for size and type.
    
    Args:
        file_obj (InMemoryUploadedFile): File object from request
        
    Raises:
        FileTooLargeError: If file size exceeds limit
        InvalidFileTypeError: If file type not allowed
        InvalidInputError: If file is missing or invalid
        
    Example:
        >>> from django.core.files.uploadedfile import SimpleUploadedFile
        >>> test_file = SimpleUploadedFile("test.pdf", b"content")
        >>> validate_file_upload(test_file)  # Valid
    """
    if not file_obj:
        raise InvalidInputError(detail="No file provided.")
    
    try:
        # Check file size
        if file_obj.size > MAX_FILE_SIZE:
            raise FileTooLargeError(
                detail=f"File size exceeds maximum allowed size (10MB). "
                       f"Your file is {file_obj.size / (1024*1024):.2f}MB."
            )
        
        # Check file extension
        if hasattr(file_obj, 'name'):
            filename = file_obj.name.lower()
            file_extension = filename.split('.')[-1] if '.' in filename else ''
            
            if file_extension not in ALLOWED_FILE_EXTENSIONS:
                raise InvalidFileTypeError(
                    detail=f"File type '.{file_extension}' not allowed. "
                           f"Allowed types: {', '.join(ALLOWED_FILE_EXTENSIONS)}"
                )
        
        # Check MIME type if available
        if hasattr(file_obj, 'content_type') and file_obj.content_type:
            if file_obj.content_type not in ALLOWED_MIME_TYPES:
                # Note: Don't strictly enforce MIME type as it can vary
                # Just skip validation
                pass
        
    except (AttributeError, TypeError) as e:
        raise InvalidInputError(detail="Invalid file object provided.")


def validate_address_line(value):
    """
    Validate address line format.
    
    Args:
        value (str): Address line to validate
        
    Raises:
        InvalidInputError: If address is invalid
        
    Example:
        >>> validate_address_line("123 Main Street")  # Valid
        >>> validate_address_line("")  # Raises error
    """
    if not value:
        raise InvalidInputError(detail="Address cannot be empty.")
    
    clean_address = value.strip()
    if len(clean_address) < 5:
        raise InvalidInputError(
            detail="Address must be at least 5 characters."
        )
    
    if len(clean_address) > 500:
        raise InvalidInputError(
            detail="Address cannot exceed 500 characters."
        )


def validate_customer_name(value):
    """
    Validate customer name format.
    
    Args:
        value (str): Customer name to validate
        
    Raises:
        InvalidInputError: If name is invalid
        
    Example:
        >>> validate_customer_name("John Doe")  # Valid
        >>> validate_customer_name("")  # Raises error
    """
    if not value:
        raise InvalidInputError(detail="Customer name cannot be empty.")
    
    clean_name = value.strip()
    if len(clean_name) < 2:
        raise InvalidInputError(
            detail="Customer name must be at least 2 characters."
        )
    
    if len(clean_name) > 255:
        raise InvalidInputError(
            detail="Customer name cannot exceed 255 characters."
        )
    
    # Check for valid characters (letters, spaces, hyphens, apostrophes)
    import re
    if not re.match(r"^[a-zA-Z\s\-']*$", clean_name):
        raise InvalidInputError(
            detail="Customer name can only contain letters, spaces, hyphens, and apostrophes."
        )
