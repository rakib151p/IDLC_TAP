from django.db import models

class Customer(models.Model):
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

# Mobile Number (multiple: primary, alternate, etc.)
class PhoneNumber(models.Model):
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

# Address (multiple: present address, permanent address, mailing address etc.)
class Address(models.Model):
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

# Documents: NID, Tax Certificate, Photo, Signature etc.
class Document(models.Model):
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