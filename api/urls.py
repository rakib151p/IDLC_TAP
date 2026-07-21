"""
URL routing configuration for Customer Management API.

This module maps API endpoints to their corresponding views.

Available Endpoints:
    Customers:
        - GET    /api/customers/                          - List all customers
        - POST   /api/customers/create/                   - Create new customer
        - GET    /api/customers/<id>/                     - Get customer details
        - PUT    /api/customers/<id>/update/              - Update customer (full)
        - PATCH  /api/customers/<id>/update/              - Update customer (partial)
        - DELETE /api/customers/<id>/delete/              - Delete customer

    Phone Numbers:
        - GET    /api/customers/<customer_id>/phone-numbers/
        - POST   /api/customers/<customer_id>/phone-numbers/
        - GET    /api/customers/<customer_id>/phone-numbers/<id>/
        - PUT    /api/customers/<customer_id>/phone-numbers/<id>/
        - PATCH  /api/customers/<customer_id>/phone-numbers/<id>/
        - DELETE /api/customers/<customer_id>/phone-numbers/<id>/

    Addresses:
        - GET    /api/customers/<customer_id>/addresses/
        - POST   /api/customers/<customer_id>/addresses/
        - GET    /api/customers/<customer_id>/addresses/<id>/
        - PUT    /api/customers/<customer_id>/addresses/<id>/
        - PATCH  /api/customers/<customer_id>/addresses/<id>/
        - DELETE /api/customers/<customer_id>/addresses/<id>/

    Documents:
        - GET    /api/customers/<customer_id>/documents/
        - POST   /api/customers/<customer_id>/documents/
        - GET    /api/customers/<customer_id>/documents/<id>/
        - PUT    /api/customers/<customer_id>/documents/<id>/
        - PATCH  /api/customers/<customer_id>/documents/<id>/
        - DELETE /api/customers/<customer_id>/documents/<id>/
"""
from django.urls import path

from api.views import (
    CustomerCreateAPIView,
    CustomerAddressDetailAPIView,
    CustomerAddressListCreateAPIView,
    CustomerDeleteAPIView,
    CustomerListAPIView,
    CustomerDocumentDetailAPIView,
    CustomerDocumentListCreateAPIView,
    CustomerRetrieveAPIView,
    CustomerPhoneNumberDetailAPIView,
    CustomerPhoneNumberListCreateAPIView,
    CustomerUpdateAPIView,
)

urlpatterns = [
    # Customer endpoints
    path("customers/", CustomerListAPIView.as_view(), name="customer-list"),
    path("customers/create/", CustomerCreateAPIView.as_view(), name="customer-create"),
    path("customers/<int:pk>/", CustomerRetrieveAPIView.as_view(), name="customer-detail"),
    path("customers/<int:pk>/update/", CustomerUpdateAPIView.as_view(), name="customer-update"),
    path("customers/<int:pk>/delete/", CustomerDeleteAPIView.as_view(), name="customer-delete"),
    
    # Phone number endpoints
    path("customers/<int:customer_id>/phone-numbers/", CustomerPhoneNumberListCreateAPIView.as_view(), name="customer-phone-number-list"),
    path("customers/<int:customer_id>/phone-numbers/<int:pk>/", CustomerPhoneNumberDetailAPIView.as_view(), name="customer-phone-number-detail"),
    
    # Address endpoints
    path("customers/<int:customer_id>/addresses/", CustomerAddressListCreateAPIView.as_view(), name="customer-address-list"),
    path("customers/<int:customer_id>/addresses/<int:pk>/", CustomerAddressDetailAPIView.as_view(), name="customer-address-detail"),
    
    # Document endpoints
    path("customers/<int:customer_id>/documents/", CustomerDocumentListCreateAPIView.as_view(), name="customer-document-list"),
    path("customers/<int:customer_id>/documents/<int:pk>/", CustomerDocumentDetailAPIView.as_view(), name="customer-document-detail"),
]