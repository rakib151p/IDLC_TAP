"""
API Views for Customer Management System

This module contains API endpoints for managing customers and their related data
including phone numbers, addresses, and documents.
"""
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework import generics, pagination, parsers
from rest_framework.exceptions import ValidationError as DRFValidationError

from api.models import Address, Customer, Document, PhoneNumber
from api.serializers import (
	AddressSerializer,
	CustomerSerializer,
	DocumentSerializer,
	PhoneNumberSerializer,
)
from api.exceptions import (
	DuplicateEmailError,
	DuplicateNationalIDError,
	DatabaseError,
)


class CustomerPagination(pagination.PageNumberPagination):
	"""
	Custom pagination class for customer list endpoints.
	
	Attributes:
		page_size (int): Number of items per page (default: 10)
		page_size_query_param (str): Query parameter to override page size
		max_page_size (int): Maximum allowed page size (100)
	
	Example:
		GET /api/customers/?page=1&page_size=20
	"""
	page_size = 10
	page_size_query_param = "page_size"
	max_page_size = 100


class CustomerQuerysetMixin:
	"""
	Mixin for filtering and ordering customers.
	
	Features:
		- Search customers by name (case-insensitive)
		- Sort customers by multiple fields (name, email, date_of_birth, created_at, updated_at)
		- Use '-' prefix for descending order
	
	Query Parameters:
		search (str): Search term to filter customers by name
		ordering (str): Field to sort by (e.g., 'name', '-created_at')
	
	Example:
		GET /api/customers/?search=John&ordering=-created_at
	"""
	allowed_ordering = {
		"name",
		"-name",
		"email",
		"-email",
		"date_of_birth",
		"-date_of_birth",
		"created_at",
		"-created_at",
		"updated_at",
		"-updated_at",
	}

	def get_queryset(self):
		queryset = Customer.objects.all()
		search_term = self.request.query_params.get("search")
		ordering = self.request.query_params.get("ordering")

		if search_term:
			queryset = queryset.filter(name__icontains=search_term)

		if ordering in self.allowed_ordering:
			queryset = queryset.order_by(ordering)

		return queryset


class CustomerListAPIView(CustomerQuerysetMixin, generics.ListAPIView):
	"""
	List all customers with pagination, search, and ordering support.
	
	HTTP Method: GET
	Endpoint: /api/customers/
	
	Features:
		- Paginated results (10 per page by default)
		- Search by customer name (query param: 'search')
		- Sort by multiple fields (query param: 'ordering')
		- Override page size with 'page_size' query parameter
	
	Query Parameters:
		page (int): Page number (default: 1)
		page_size (int): Number of items per page (1-100, default: 10)
		search (str): Filter customers by name
		ordering (str): Sort field with optional '-' prefix for descending
	
	Response:
		{
			"count": 25,
			"next": "http://api.example.com/customers/?page=2",
			"previous": null,
			"results": [
				{
					"id": 1,
					"name": "John Doe",
					"email": "john@example.com",
					"date_of_birth": "1990-01-01",
					"national_id_number": "1234567890",
					"phone_numbers": [],
					"addresses": [],
					"documents": [],
					"created_at": "2024-01-01T10:00:00Z",
					"updated_at": "2024-01-01T10:00:00Z"
				}
			]
		}
	
	Example Requests:
		GET /api/customers/
		GET /api/customers/?page=2&page_size=20
		GET /api/customers/?search=John
		GET /api/customers/?ordering=-created_at
	"""
	serializer_class = CustomerSerializer
	pagination_class = CustomerPagination


class CustomerCreateAPIView(generics.CreateAPIView):
	"""
	Create a new customer.
	
	HTTP Method: POST
	Endpoint: /api/customers/create/
	
	Request Body:
		{
			"name": "John Doe",
			"email": "john@example.com",
			"date_of_birth": "1990-01-01",
			"national_id_number": "1234567890"
		}
	
	Response (201 Created):
		{
			"id": 1,
			"name": "John Doe",
			"email": "john@example.com",
			"date_of_birth": "1990-01-01",
			"national_id_number": "1234567890",
			"phone_numbers": [],
			"addresses": [],
			"documents": [],
			"created_at": "2024-01-01T10:00:00Z",
			"updated_at": "2024-01-01T10:00:00Z"
		}
	
	Notes:
		- Email and national_id_number must be unique
		- All fields are required
		- Handles IntegrityError for duplicate fields
	"""
	serializer_class = CustomerSerializer
	queryset = Customer.objects.all()
	
	def perform_create(self, serializer):
		"""
		Create a new customer with error handling.
		
		Args:
			serializer (CustomerSerializer): Validated serializer instance
			
		Raises:
			DuplicateEmailError: If email already exists
			DuplicateNationalIDError: If national_id_number already exists
			DatabaseError: If database operation fails
		"""
		try:
			serializer.save()
		except IntegrityError as e:
			if "email" in error_message.lower():
				raise DuplicateEmailError()
			elif "national_id" in error_message.lower():
				raise DuplicateNationalIDError()
			else:
				raise DatabaseError(detail="Failed to create customer. Duplicate data detected.")
		except Exception as e:
			raise DatabaseError(detail="Failed to create customer. Please try again later.")


class CustomerRetrieveAPIView(generics.RetrieveAPIView):
	"""
	Retrieve a specific customer by ID.
	
	HTTP Method: GET
	Endpoint: /api/customers/<id>/
	
	Path Parameters:
		id (int): Customer ID
	
	Response (200 OK):
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
					"file": "/media/customer_documents/...",
					"uploaded_at": "2024-01-01T10:00:00Z"
				}
			],
			"created_at": "2024-01-01T10:00:00Z",
			"updated_at": "2024-01-01T10:00:00Z"
		}
	
	Example Request:
		GET /api/customers/1/
	"""
	serializer_class = CustomerSerializer
	queryset = Customer.objects.all()


class CustomerUpdateAPIView(generics.UpdateAPIView):
	"""
	Update a customer (partial or full update).
	
	HTTP Methods:
		PUT (full update) - All fields required
		PATCH (partial update) - Only changed fields required
	
	Endpoint: /api/customers/<id>/update/
	
	Path Parameters:
		id (int): Customer ID
	
	Request Body (PATCH - partial update):
		{
			"name": "Jane Doe"
		}
	
	Request Body (PUT - full update):
		{
			"name": "Jane Doe",
			"email": "jane@example.com",
			"date_of_birth": "1990-01-01",
			"national_id_number": "1234567890"
		}
	
	Response (200 OK):
		Updated customer object with all fields
	
	Example Requests:
		PATCH /api/customers/1/update/
		PUT /api/customers/1/update/
	"""
	serializer_class = CustomerSerializer
	queryset = Customer.objects.all()
	
	def perform_update(self, serializer):
		"""
		Update a customer with error handling.
		
		Args:
			serializer (CustomerSerializer): Validated serializer instance
			
		Raises:
			DuplicateEmailError: If email already exists
			DuplicateNationalIDError: If national_id_number already exists
			DatabaseError: If database operation fails
		"""
		try:
			serializer.save()
		except IntegrityError as e:
			
			if "email" in error_message.lower():
				raise DuplicateEmailError()
			elif "national_id" in error_message.lower():
				raise DuplicateNationalIDError()
			else:
				raise DatabaseError(detail="Failed to update customer. Duplicate data detected.")
		except Exception as e:
			raise DatabaseError(detail="Failed to update customer. Please try again later.")


class CustomerDeleteAPIView(generics.DestroyAPIView):
	"""
	Delete a customer and all associated data.
	
	HTTP Method: DELETE
	Endpoint: /api/customers/<id>/delete/
	
	Path Parameters:
		id (int): Customer ID
	
	Response (204 No Content):
		No response body
	
	Notes:
		- Deletes the customer and all related phone numbers, addresses, and documents
		- This action cannot be undone
	
	Example Request:
		DELETE /api/customers/1/delete/
	"""
	serializer_class = CustomerSerializer
	queryset = Customer.objects.all()


class CustomerRelatedQuerysetMixin:
	"""
	Mixin for views managing customer-related resources.
	
	This mixin ensures that phone numbers, addresses, and documents are properly
	filtered by customer and automatically associated with the correct customer.
	
	Attributes:
		customer_lookup_url_kwarg (str): URL parameter name for customer ID
	
	Methods:
		get_customer(): Retrieves the customer from URL parameters
		filter_by_customer(): Filters queryset by customer
		perform_create(): Automatically sets customer when creating related objects
		get_queryset(): Returns only objects for the specified customer
	"""
	customer_lookup_url_kwarg = "customer_id"

	def get_customer(self):
		"""
		Get the customer object from URL parameters.
		
		Returns:
			Customer: The customer object
			
		Raises:
			Http404: If customer does not exist
		"""
		try:
			return get_object_or_404(Customer, pk=self.kwargs[self.customer_lookup_url_kwarg])
		except Exception as e:
			raise

	def filter_by_customer(self, queryset):
		"""
		Filter queryset by customer ID from URL.
		
		Args:
			queryset (QuerySet): Base queryset to filter
			
		Returns:
			QuerySet: Filtered queryset for the specific customer
		"""
		return queryset.filter(customer_id=self.kwargs[self.customer_lookup_url_kwarg])

	def perform_create(self, serializer):
		"""
		Create related object with error handling.
		
		Args:
			serializer: Validated serializer instance
			
		Raises:
			DatabaseError: If creation fails
		"""
		try:
			serializer.save(customer=self.get_customer())
		except IntegrityError as e:
			raise DatabaseError(detail="Failed to create resource. Please check your data.")
		except Exception as e:
			raise DatabaseError(detail="Failed to create resource. Please try again later.")

	def get_queryset(self):
		"""
		Get queryset filtered by customer.
		
		Returns:
			QuerySet: Filtered queryset for the specified customer
		"""
		return self.filter_by_customer(self.queryset)


class CustomerPhoneNumberListCreateAPIView(CustomerRelatedQuerysetMixin, generics.ListCreateAPIView):
	"""
	List and create phone numbers for a specific customer.
	
	HTTP Methods:
		GET - List all phone numbers for a customer
		POST - Create a new phone number for a customer
	
	Endpoint: /api/customers/<customer_id>/phone-numbers/
	
	Path Parameters:
		customer_id (int): Customer ID
	
	GET Response (200 OK):
		[
			{
				"id": 1,
				"phone_type": "PRIMARY",
				"number": "+880123456789"
			},
			{
				"id": 2,
				"phone_type": "ALTERNATE",
				"number": "+880987654321"
			}
		]
	
	POST Request Body:
		{
			"phone_type": "PRIMARY",
			"number": "+880123456789"
		}
	
	POST Response (201 Created):
		{
			"id": 1,
			"phone_type": "PRIMARY",
			"number": "+880123456789"
		}
	
	Phone Types:
		- PRIMARY
		- ALTERNATE
		- OFFICE
		- HOME
	
	Example Requests:
		GET /api/customers/1/phone-numbers/
		POST /api/customers/1/phone-numbers/
	"""
	serializer_class = PhoneNumberSerializer
	queryset = PhoneNumber.objects.all()


class CustomerPhoneNumberDetailAPIView(CustomerRelatedQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update, or delete a specific phone number for a customer.
	
	HTTP Methods:
		GET - Retrieve phone number
		PUT - Full update
		PATCH - Partial update
		DELETE - Delete phone number
	
	Endpoint: /api/customers/<customer_id>/phone-numbers/<id>/
	
	Path Parameters:
		customer_id (int): Customer ID
		id (int): Phone number ID
	
	GET Response (200 OK):
		{
			"id": 1,
			"phone_type": "PRIMARY",
			"number": "+880123456789"
		}
	
	PATCH Request Body:
		{
			"number": "+880123456789"
		}
	
	PATCH Response (200 OK):
		Updated phone number object
	
	Example Requests:
		GET /api/customers/1/phone-numbers/1/
		PATCH /api/customers/1/phone-numbers/1/
		DELETE /api/customers/1/phone-numbers/1/
	"""
	serializer_class = PhoneNumberSerializer
	queryset = PhoneNumber.objects.all()


class CustomerAddressListCreateAPIView(CustomerRelatedQuerysetMixin, generics.ListCreateAPIView):
	"""
	List and create addresses for a specific customer.
	
	HTTP Methods:
		GET - List all addresses for a customer
		POST - Create a new address for a customer
	
	Endpoint: /api/customers/<customer_id>/addresses/
	
	Path Parameters:
		customer_id (int): Customer ID
	
	GET Response (200 OK):
		[
			{
				"id": 1,
				"address_type": "PRESENT",
				"address_line": "123 Main St",
				"city": "Dhaka",
				"district": "Dhaka",
				"postal_code": "1000",
				"country": "Bangladesh"
			}
		]
	
	POST Request Body:
		{
			"address_type": "PRESENT",
			"address_line": "123 Main St",
			"city": "Dhaka",
			"district": "Dhaka",
			"postal_code": "1000",
			"country": "Bangladesh"
		}
	
	POST Response (201 Created):
		Full address object with ID
	
	Address Types:
		- PRESENT (Current residential address)
		- PERMANENT (Permanent address)
		- MAILING (Mailing address)
		- OFFICE (Office address)
	
	Example Requests:
		GET /api/customers/1/addresses/
		POST /api/customers/1/addresses/
	"""
	serializer_class = AddressSerializer
	queryset = Address.objects.all()


class CustomerAddressDetailAPIView(CustomerRelatedQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update, or delete a specific address for a customer.
	
	HTTP Methods:
		GET - Retrieve address
		PUT - Full update
		PATCH - Partial update
		DELETE - Delete address
	
	Endpoint: /api/customers/<customer_id>/addresses/<id>/
	
	Path Parameters:
		customer_id (int): Customer ID
		id (int): Address ID
	
	GET Response (200 OK):
		{
			"id": 1,
			"address_type": "PRESENT",
			"address_line": "123 Main St",
			"city": "Dhaka",
			"district": "Dhaka",
			"postal_code": "1000",
			"country": "Bangladesh"
		}
	
	PATCH Request Body:
		{
			"address_line": "456 New St",
			"city": "Chittagong"
		}
	
	PATCH Response (200 OK):
		Updated address object
	
	Example Requests:
		GET /api/customers/1/addresses/1/
		PATCH /api/customers/1/addresses/1/
		DELETE /api/customers/1/addresses/1/
	"""
	serializer_class = AddressSerializer
	queryset = Address.objects.all()


class CustomerDocumentListCreateAPIView(CustomerRelatedQuerysetMixin, generics.ListCreateAPIView):
	"""
	List and create documents (files) for a specific customer.
	
	HTTP Methods:
		GET - List all documents for a customer
		POST - Upload a new document for a customer
	
	Endpoint: /api/customers/<customer_id>/documents/
	
	Path Parameters:
		customer_id (int): Customer ID
	
	GET Response (200 OK):
		[
			{
				"id": 1,
				"document_type": "NID",
				"file": "/media/customer_documents/nid_001.pdf",
				"uploaded_at": "2024-01-01T10:00:00Z"
			}
		]
	
	POST Request (multipart/form-data):
		- document_type (string, required): Type of document
		- file (file, required): Document file to upload
	
	POST Response (201 Created):
		{
			"id": 1,
			"document_type": "NID",
			"file": "/media/customer_documents/nid_001.pdf",
			"uploaded_at": "2024-01-01T10:00:00Z"
		}
	
	Document Types:
		- NID (National ID)
		- TAX_CERTIFICATE (Tax Certificate)
		- PHOTO (Photo)
		- SIGNATURE (Signature)
	
	Notes:
		- POST requests must use multipart/form-data content type
		- Files are stored in media/customer_documents/ directory
		- uploaded_at is automatically set to current timestamp
	
	Example Requests:
		GET /api/customers/1/documents/
		POST /api/customers/1/documents/ (with file upload)
	"""
	serializer_class = DocumentSerializer
	queryset = Document.objects.all()
	parser_classes = [parsers.MultiPartParser, parsers.FormParser]


class CustomerDocumentDetailAPIView(CustomerRelatedQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update, or delete a specific document for a customer.
	
	HTTP Methods:
		GET - Retrieve document info
		PUT - Full update (requires new file)
		PATCH - Partial update
		DELETE - Delete document
	
	Endpoint: /api/customers/<customer_id>/documents/<id>/
	
	Path Parameters:
		customer_id (int): Customer ID
		id (int): Document ID
	
	GET Response (200 OK):
		{
			"id": 1,
			"document_type": "NID",
			"file": "/media/customer_documents/nid_001.pdf",
			"uploaded_at": "2024-01-01T10:00:00Z"
		}
	
	PATCH Request (multipart/form-data):
		{
			"document_type": "PHOTO",
			"file": <new_file> (optional)
		}
	
	PATCH Response (200 OK):
		Updated document object
	
	Notes:
		- Both GET and modifications support multipart/form-data for file handling
		- For PATCH, you can update document_type without changing the file
		- For PATCH, you can upload a new file without changing the type
	
	Example Requests:
		GET /api/customers/1/documents/1/
		PATCH /api/customers/1/documents/1/ (with or without file)
		DELETE /api/customers/1/documents/1/
	"""
	serializer_class = DocumentSerializer
	queryset = Document.objects.all()
	parser_classes = [parsers.MultiPartParser, parsers.FormParser]

