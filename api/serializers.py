"""
Serializers for Customer Management API.

Serializers define how Django models are converted to/from JSON representations
for API requests and responses.
"""
from rest_framework import serializers

from api.models import Customer, Address, Document, PhoneNumber


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
    """
    class Meta:
        model = Document
        fields = ["id", "customer", "document_type", "file", "uploaded_at"]
        read_only_fields = ["id", "customer", "uploaded_at"]


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
