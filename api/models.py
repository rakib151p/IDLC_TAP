"""
Models for Customer Management System.

This module defines the data models for storing customer information including
personal details, contact information, addresses, and documents.
"""
from django.db import models


class Customer(models.Model):
	"""
	Customer model representing a person or entity in the system.
	
	This is the primary model that stores basic customer information.
	All other models (PhoneNumber, Address, Document) are related to this model.
	
	Attributes:
		id (int): Auto-generated primary key
		name (str): Customer's full name (max 255 characters)
		email (str): Unique email address for the customer
		date_of_birth (date): Customer's date of birth
		national_id_number (str): Unique national ID (e.g., NID, passport number)
		created_at (datetime): Automatically set when customer is created
		updated_at (datetime): Automatically updated when customer is modified
	
	Example:
		customer = Customer.objects.create(
			name="John Doe",
			email="john@example.com",
			date_of_birth="1990-01-01",
			national_id_number="1234567890"
		)
	"""
	name = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	date_of_birth = models.DateField()
	national_id_number = models.CharField(max_length=50, unique=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return self.name


class PhoneNumber(models.Model):
	"""
	Phone Number model for storing customer phone numbers.
	
	Each customer can have multiple phone numbers with different types.
	This allows storing primary, alternate, office, and home phone numbers.
	
	Attributes:
		id (int): Auto-generated primary key
		customer (ForeignKey): Reference to the Customer model
		phone_type (str): Type of phone number (choices: PRIMARY, ALTERNATE, OFFICE, HOME)
		number (str): The actual phone number (max 20 characters)
	
	Phone Type Choices:
		- PRIMARY: Primary contact number
		- ALTERNATE: Secondary/alternate contact number
		- OFFICE: Office or business phone number
		- HOME: Home phone number
	
	Example:
		phone = PhoneNumber.objects.create(
			customer=customer_obj,
			phone_type="PRIMARY",
			number="+880123456789"
		)
	"""
	class PhoneType(models.TextChoices):
		PRIMARY = "PRIMARY", "Primary"
		ALTERNATE = "ALTERNATE", "Alternate"
		OFFICE = "OFFICE", "Office"
		HOME = "HOME", "Home"

	customer = models.ForeignKey(
		Customer,
		on_delete=models.CASCADE,
		related_name="phone_numbers"
	)

	phone_type = models.CharField(
		max_length=20,
		choices=PhoneType.choices
	)

	number = models.CharField(max_length=20)

	def __str__(self):
		return f"{self.customer.name} - {self.phone_type} : {self.number}"


class Address(models.Model):
	"""
	Address model for storing customer addresses.
	
	Each customer can have multiple addresses with different types.
	This allows storing present, permanent, mailing, and office addresses.
	
	Attributes:
		id (int): Auto-generated primary key
		customer (ForeignKey): Reference to the Customer model
		address_type (str): Type of address (choices: PRESENT, PERMANENT, MAILING, OFFICE)
		address_line (str): Street address or detailed location
		city (str): City name (max 100 characters)
		district (str): District or province name (max 100 characters)
		postal_code (str): Postal or ZIP code (max 20 characters)
		country (str): Country name (default: Bangladesh)
	
	Address Type Choices:
		- PRESENT: Current residential address
		- PERMANENT: Permanent address
		- MAILING: Mailing address for correspondence
		- OFFICE: Office or business address
	
	Example:
		address = Address.objects.create(
			customer=customer_obj,
			address_type="PRESENT",
			address_line="123 Main Street",
			city="Dhaka",
			district="Dhaka",
			postal_code="1000",
			country="Bangladesh"
		)
	"""
	class AddressType(models.TextChoices):
		PRESENT = "PRESENT", "Present"
		PERMANENT = "PERMANENT", "Permanent"
		MAILING = "MAILING", "Mailing"
		OFFICE = "OFFICE", "Office"

	customer = models.ForeignKey(
		Customer,
		on_delete=models.CASCADE,
		related_name="addresses"
	)

	address_type = models.CharField(
		max_length=20,
		choices=AddressType.choices
	)

	address_line = models.TextField()
	city = models.CharField(max_length=100)
	district = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=20)
	country = models.CharField(max_length=100, default="Bangladesh")

	def __str__(self):
		return f"{self.customer.name} - {self.address_type} Address : {self.address_line}, {self.city}, {self.district}, {self.postal_code}, {self.country}"


class Document(models.Model):
	"""
	Document model for storing customer documents and files.
	
	Each customer can have multiple documents of different types.
	Documents are stored as file uploads (e.g., images, PDFs).
	
	Attributes:
		id (int): Auto-generated primary key
		customer (ForeignKey): Reference to the Customer model
		document_type (str): Type of document (choices: NID, TAX_CERTIFICATE, PHOTO, SIGNATURE)
		file (FileField): The uploaded document file
		uploaded_at (datetime): Automatically set when document is uploaded
	
	Document Type Choices:
		- NID: National ID card or identification document
		- TAX_CERTIFICATE: Tax-related certificate or document
		- PHOTO: Profile photo or other photograph
		- SIGNATURE: Digital signature or signature scan
	
	File Storage:
		Files are stored in the 'customer_documents/' directory within the media folder.
		Example path: /media/customer_documents/nid_12345.pdf
	
	Example:
		document = Document.objects.create(
			customer=customer_obj,
			document_type="NID",
			file=<file_object>
		)
	"""
	class DocumentType(models.TextChoices):
		NID = "NID", "National ID"
		TAX_CERTIFICATE = "TAX_CERTIFICATE", "Tax Certificate"
		PHOTO = "PHOTO", "Photo"
		SIGNATURE = "SIGNATURE", "Signature"

	customer = models.ForeignKey(
		Customer,
		on_delete=models.CASCADE,
		related_name="documents"
	)

	document_type = models.CharField(
		max_length=30,
		choices=DocumentType.choices
	)

	file = models.FileField(upload_to="customer_documents/")
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.customer.name} - {self.document_type}"