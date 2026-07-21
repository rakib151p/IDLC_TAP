from datetime import date
import base64

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Address, Customer, Document, PhoneNumber


class CustomerApiTests(APITestCase):
	def setUp(self):
		self.customer_a = Customer.objects.create(
			name="Alice Johnson",
			email="alice@example.com",
			date_of_birth=date(1990, 1, 1),
			national_id_number="NID-001",
		)
		self.customer_b = Customer.objects.create(
			name="Bob Stone",
			email="bob@example.com",
			date_of_birth=date(1988, 5, 5),
			national_id_number="NID-002",
		)

	def test_create_customer(self):
		response = self.client.post(
			reverse("customer-create"),
			{
				"name": "Charlie Ray",
				"email": "charlie@example.com",
				"date_of_birth": "1995-03-15",
				"national_id_number": "NID-003",
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Customer.objects.count(), 3)

	def test_create_customer_with_related_items(self):
		document_content = base64.b64encode(b"dummy document content").decode("utf-8")
		response = self.client.post(
			reverse("customer-create"),
			{
				"name": "David Khan",
				"email": "david@example.com",
				"date_of_birth": "1992-07-10",
				"national_id_number": "NID-004",
				"phone_numbers": [
					{
						"phone_type": PhoneNumber.PhoneType.PRIMARY,
						"number": "01711111111",
					},
				],
				"addresses": [
					{
						"address_type": Address.AddressType.PRESENT,
						"address_line": "House 1, Road 2",
						"city": "Dhaka",
						"district": "Dhaka",
						"postal_code": "1207",
						"country": "Bangladesh",
					},
				],
				"documents": [
					{
						"document_type": Document.DocumentType.NID,
						"file": f"data:application/pdf;base64,{document_content}",
					},
				],
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		customer = Customer.objects.get(email="david@example.com")
		self.assertEqual(customer.phone_numbers.count(), 1)
		self.assertEqual(customer.addresses.count(), 1)
		self.assertEqual(customer.documents.count(), 1)

	def test_get_customer_by_id(self):
		response = self.client.get(reverse("customer-detail", args=[self.customer_a.id]))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["name"], self.customer_a.name)

	def test_list_customers_supports_search_filter_sort_and_pagination(self):
		response = self.client.get(
			reverse("customer-list"),
			{
				"search": "Alice",
				"ordering": "name",
				"page_size": 1,
			},
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["count"], 1)
		self.assertEqual(response.data["results"][0]["name"], self.customer_a.name)

	def test_update_customer(self):
		response = self.client.patch(
			reverse("customer-update", args=[self.customer_a.id]),
			{"name": "Alice Johnson Updated"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.customer_a.refresh_from_db()
		self.assertEqual(self.customer_a.name, "Alice Johnson Updated")

	def test_delete_customer(self):
		response = self.client.delete(reverse("customer-delete", args=[self.customer_b.id]))

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Customer.objects.filter(id=self.customer_b.id).exists())

	def test_create_phone_number_for_customer(self):
		response = self.client.post(
			reverse("customer-phone-number-list", args=[self.customer_a.id]),
			{
				"phone_type": PhoneNumber.PhoneType.PRIMARY,
				"number": "01700000000",
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(PhoneNumber.objects.filter(customer=self.customer_a).count(), 1)

	def test_create_address_for_customer(self):
		response = self.client.post(
			reverse("customer-address-list", args=[self.customer_a.id]),
			{
				"address_type": Address.AddressType.PRESENT,
				"address_line": "House 10, Road 5",
				"city": "Dhaka",
				"district": "Dhaka",
				"postal_code": "1205",
				"country": "Bangladesh",
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Address.objects.filter(customer=self.customer_a).count(), 1)

	def test_create_document_for_customer(self):
		file_content = SimpleUploadedFile("nid.pdf", b"dummy document content", content_type="application/pdf")
		response = self.client.post(
			reverse("customer-document-list", args=[self.customer_a.id]),
			{
				"document_type": Document.DocumentType.NID,
				"file": file_content,
			},
			format="multipart",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Document.objects.filter(customer=self.customer_a).count(), 1)
