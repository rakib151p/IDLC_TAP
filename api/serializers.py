"""
Serializers for Customer Management API.

Serializers define how Django models are converted to/from JSON representations
for API requests and responses.
"""
from rest_framework import serializers

from api.models import Customer, Address, Document, PhoneNumber
from api.validators import (
    validate_customer_name,
    validate_email,
    validate_date_of_birth,
    validate_national_id,
    validate_phone_number,
    validate_postal_code,
    validate_address_line,
    validate_file_upload,
)
from api.exceptions import (
    DuplicateEmailError,
    DuplicateNationalIDError,
    InvalidInputError,
)

class PhoneNumberSerializer(serializers.ModelSerializer):
    """
    Serializer for PhoneNumber model.
    
    Attributes:
        id (int): Phone number ID (read-only)
        customer (int): Related customer ID (read-only, set automatically)
        phone_type (str): Type of phone number (PRIMARY, ALTERNATE, OFFICE, HOME)
        number (str): Phone number in E.164 format or local format
    
    Example Request Body (POST):
        {
            "phone_type": "PRIMARY",
            "number": "+880123456789"
        }
    
    Example Response:
        {
            "id": 1,
            "phone_type": "PRIMARY",
            "number": "+880123456789"
        }
    """
    class Meta:
        model = PhoneNumber
        fields = ["id", "customer", "phone_type", "number"]
        read_only_fields = ["id", "customer"]
    
    def validate_number(self, value):
        """
        Validate phone number format.
        
        Args:
            value (str): Phone number to validate
            
        Returns:
            str: Validated phone number
            
        Raises:
            InvalidInputError: If phone number format is invalid
        """
        try:
            validate_phone_number(value)
            return value
        except InvalidInputError as e:
            raise serializers.ValidationError(str(e.detail))
    
    def validate_phone_type(self, value):
        """
        Validate phone type choice.
        
        Args:
            value (str): Phone type to validate
            
        Returns:
            str: Validated phone type
            
        Raises:
            ValidationError: If phone type is not a valid choice
        """
        valid_types = [choice[0] for choice in PhoneNumber.PhoneType.choices]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid phone type. Must be one of: {', '.join(valid_types)}"
            )
        return value


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for Address model.
    
    Attributes:
        id (int): Address ID (read-only)
        customer (int): Related customer ID (read-only, set automatically)
        address_type (str): Type of address (PRESENT, PERMANENT, MAILING, OFFICE)
        address_line (str): Street address or detailed address
        city (str): City name
        district (str): District/Province name
        postal_code (str): Postal or ZIP code
        country (str): Country name (default: Bangladesh)
    
    Example Request Body (POST):
        {
            "address_type": "PRESENT",
            "address_line": "123 Main Street",
            "city": "Dhaka",
            "district": "Dhaka",
            "postal_code": "1000",
            "country": "Bangladesh"
        }
    
    Example Response:
        {
            "id": 1,
            "address_type": "PRESENT",
            "address_line": "123 Main Street",
            "city": "Dhaka",
            "district": "Dhaka",
            "postal_code": "1000",
            "country": "Bangladesh"
        }
    """
    class Meta:
        model = Address
        fields = [
            "id",
            "customer",
            "address_type",
            "address_line",
            "city",
            "district",
            "postal_code",
            "country",
        ]
        read_only_fields = ["id", "customer"]
    
    def validate_address_line(self, value):
        """
        Validate address line format.
        
        Args:
            value (str): Address line to validate
            
        Returns:
            str: Validated address line
            
        Raises:
            ValidationError: If address line is invalid
        """
        try:
            validate_address_line(value)
            return value
        except InvalidInputError as e:
            raise serializers.ValidationError(str(e.detail))
    
    def validate_postal_code(self, value):
        """
        Validate postal code format.
        
        Args:
            value (str): Postal code to validate
            
        Returns:
            str: Validated postal code
            
        Raises:
            ValidationError: If postal code is invalid
        """
        try:
            validate_postal_code(value)
            return value
        except InvalidInputError as e:
            raise serializers.ValidationError(str(e.detail))
    
    def validate_address_type(self, value):
        """
        Validate address type choice.
        
        Args:
            value (str): Address type to validate
            
        Returns:
            str: Validated address type
            
        Raises:
            ValidationError: If address type is not a valid choice
        """
        valid_types = [choice[0] for choice in Address.AddressType.choices]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid address type. Must be one of: {', '.join(valid_types)}"
            )
        return value
    
    def validate_city(self, value):
        """
        Validate city name.
        
        Args:
            value (str): City name to validate
            
        Returns:
            str: Validated city name
            
        Raises:
            ValidationError: If city name is empty or too long
        """
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError(
                "City name must be at least 2 characters."
            )
        if len(value) > 100:
            raise serializers.ValidationError(
                "City name cannot exceed 100 characters."
            )
        return value
    
    def validate_district(self, value):
        """
        Validate district name.
        
        Args:
            value (str): District name to validate
            
        Returns:
            str: Validated district name
            
        Raises:
            ValidationError: If district name is empty or too long
        """
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError(
                "District name must be at least 2 characters."
            )
        if len(value) > 100:
            raise serializers.ValidationError(
                "District name cannot exceed 100 characters."
            )
        return value


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for Document model.
    
    Attributes:
        id (int): Document ID (read-only)
        customer (int): Related customer ID (read-only, set automatically)
        document_type (str): Type of document (NID, TAX_CERTIFICATE, PHOTO, SIGNATURE)
        file (file): Document file (for multipart/form-data uploads)
        uploaded_at (datetime): Timestamp when document was uploaded (read-only)
    
    Example Request Body (POST - multipart/form-data):
        - document_type: "NID"
        - file: <binary file content>
    
    Example Response:
        {
            "id": 1,
            "document_type": "NID",
            "file": "/media/customer_documents/nid_123456.pdf",
            "uploaded_at": "2024-01-01T10:00:00Z"
        }
    
    Notes:
        - POST and PUT requests must use multipart/form-data content type
        - Files are stored in media/customer_documents/ directory
        - uploaded_at is automatically set and cannot be modified
        - Maximum file size: 10MB
        - Allowed file types: PDF, JPG, JPEG, PNG, GIF, DOC, DOCX, TXT
    """
    class Meta:
        model = Document
        fields = ["id", "customer", "document_type", "file", "uploaded_at"]
        read_only_fields = ["id", "customer", "uploaded_at"]
    
    def validate_file(self, value):
        """
        Validate uploaded file for size and type.
        
        Args:
            value (InMemoryUploadedFile): File object to validate
            
        Returns:
            InMemoryUploadedFile: Validated file object
            
        Raises:
            ValidationError: If file validation fails
        """
        try:
            validate_file_upload(value)
            return value
        except Exception as e:
            raise serializers.ValidationError(str(e.detail) if hasattr(e, 'detail') else str(e))
    
    def validate_document_type(self, value):
        """
        Validate document type choice.
        
        Args:
            value (str): Document type to validate
            
        Returns:
            str: Validated document type
            
        Raises:
            ValidationError: If document type is not a valid choice
        """
        valid_types = [choice[0] for choice in Document.DocumentType.choices]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid document type. Must be one of: {', '.join(valid_types)}"
            )
        return value


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model with nested related objects.
    
    Attributes:
        id (int): Customer ID (read-only)
        name (str): Customer's full name
        email (str): Unique email address
        date_of_birth (date): Date of birth in YYYY-MM-DD format
        national_id_number (str): Unique national ID number
        phone_numbers (list): List of PhoneNumberSerializer objects (read-only)
        addresses (list): List of AddressSerializer objects (read-only)
        documents (list): List of DocumentSerializer objects (read-only)
        created_at (datetime): Timestamp when customer was created (read-only)
        updated_at (datetime): Timestamp when customer was last updated (read-only)
    
    Example Request Body (POST):
        {
            "name": "John Doe",
            "email": "john@example.com",
            "date_of_birth": "1990-01-01",
            "national_id_number": "1234567890"
        }
    
    Example Response (GET):
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "date_of_birth": "1990-01-01",
            "national_id_number": "1234567890",
            "phone_numbers": [
                {
                    "id": 1,
                    "phone_type": "PRIMARY",
                    "number": "+880123456789"
                }
            ],
            "addresses": [
                {
                    "id": 1,
                    "address_type": "PRESENT",
                    "address_line": "123 Main St",
                    "city": "Dhaka",
                    "district": "Dhaka",
                    "postal_code": "1000",
                    "country": "Bangladesh"
                }
            ],
            "documents": [
                {
                    "id": 1,
                    "document_type": "NID",
                    "file": "/media/customer_documents/nid_123.pdf",
                    "uploaded_at": "2024-01-01T10:00:00Z"
                }
            ],
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z"
        }
    
    Notes:
        - email and national_id_number must be globally unique
        - All fields except phone_numbers, addresses, and documents are required in POST requests
        - Related objects (phone_numbers, addresses, documents) are managed through separate endpoints
    """
    phone_numbers = PhoneNumberSerializer(many=True, read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"
    
    def validate_name(self, value):
        """
        Validate customer name format.
        
        Args:
            value (str): Customer name to validate
            
        Returns:
            str: Validated customer name
            
        Raises:
            ValidationError: If customer name is invalid
        """
        try:
            validate_customer_name(value)
            return value
        except InvalidInputError as e:
            raise serializers.ValidationError(str(e.detail))
    
    def validate_email(self, value):
        """
        Validate email format and uniqueness.
        
        Args:
            value (str): Email address to validate
            
        Returns:
            str: Validated email address
            
        Raises:
            ValidationError: If email format is invalid or already exists
        """
        try:
            validate_email(value)
            return value
        except InvalidInputError as e:
            raise serializers.ValidationError(str(e.detail))
    
    def validate_date_of_birth(self, value):
        """
        Validate date of birth format and ensure it's in the past.
        
        Args:
            value (date): Date of birth to validate
            
        Returns:
            date: Validated date of birth
            
        Raises:
            ValidationError: If date is invalid or in the future
        """
        try:
            validate_date_of_birth(value)
            return value
        except Exception as e:
            raise serializers.ValidationError(str(e.detail))
            
    def validate_national_id_number(self, value):
        """
        Validate national ID format.
        
        Args:
            value (str): National ID number to validate
            
        Returns:
            str: Validated national ID number
            
        Raises:
            ValidationError: If national ID is invalid
        """
        try:
            validate_national_id(value)
            return value
        except InvalidInputError as e:
            raise serializers.ValidationError(str(e.detail))
            