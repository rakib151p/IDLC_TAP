# Customer Management API Documentation

## Overview

This is a RESTful API for managing customer information, including personal details, contact information, addresses, and documents. The API is built with Django REST Framework and uses JSON for request/response bodies.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Response Format

### Success Response (2xx)
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  ...
}
```

### Error Response (4xx, 5xx)
```json
{
  "error": "Error message describing what went wrong"
}
```

---

## Customer Endpoints

### 1. List All Customers

**Endpoint:** `GET /customers/`

**Description:** Retrieve a paginated list of all customers with optional search and sorting.

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| page | integer | Page number (default: 1) | `?page=1` |
| page_size | integer | Items per page (1-100, default: 10) | `?page_size=20` |
| search | string | Search by customer name (case-insensitive) | `?search=john` |
| ordering | string | Sort field with optional '-' for descending | `?ordering=-created_at` |

**Allowed Ordering Fields:**
- `name`, `-name`
- `email`, `-email`
- `date_of_birth`, `-date_of_birth`
- `created_at`, `-created_at`
- `updated_at`, `-updated_at`

**Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/customers/?page=2",
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
```

**Example Requests:**
```bash
# Get first page with 10 results
GET /api/customers/

# Get page 2 with 20 results per page
GET /api/customers/?page=2&page_size=20

# Search by name
GET /api/customers/?search=John

# Sort by creation date (newest first)
GET /api/customers/?ordering=-created_at

# Combine search and sorting
GET /api/customers/?search=john&ordering=-created_at
```

---

### 2. Create a New Customer

**Endpoint:** `POST /customers/create/`

**Description:** Create a new customer with basic information.

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "date_of_birth": "1992-05-15",
  "national_id_number": "9876543210"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "date_of_birth": "1992-05-15",
  "national_id_number": "9876543210",
  "phone_numbers": [],
  "addresses": [],
  "documents": [],
  "created_at": "2024-01-02T10:00:00Z",
  "updated_at": "2024-01-02T10:00:00Z"
}
```

**Required Fields:**
- `name` (string, max 255 chars)
- `email` (string, unique, valid email format)
- `date_of_birth` (date, YYYY-MM-DD format)
- `national_id_number` (string, unique, max 50 chars)

**Error Response (400 Bad Request):**
```json
{
  "email": ["This field must be unique."],
  "national_id_number": ["This field must be unique."]
}
```

---

### 3. Get Customer Details

**Endpoint:** `GET /customers/{id}/`

**Description:** Retrieve detailed information for a specific customer including related phone numbers, addresses, and documents.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | Customer ID |

**Response (200 OK):**
```json
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
      "file": "/media/customer_documents/nid_001.pdf",
      "uploaded_at": "2024-01-01T10:00:00Z"
    }
  ],
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

**Example Request:**
```bash
GET /api/customers/1/
```

---

### 4. Update Customer (Partial)

**Endpoint:** `PATCH /customers/{id}/update/`

**Description:** Update one or more fields of a customer (partial update).

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | Customer ID |

**Request Body (example - update only name):**
```json
{
  "name": "John Smith"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Smith",
  "email": "john@example.com",
  "date_of_birth": "1990-01-01",
  "national_id_number": "1234567890",
  "phone_numbers": [],
  "addresses": [],
  "documents": [],
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-02T15:30:00Z"
}
```

**Example Request:**
```bash
PATCH /api/customers/1/update/
Content-Type: application/json

{
  "name": "John Smith",
  "email": "john.smith@example.com"
}
```

---

### 5. Update Customer (Full)

**Endpoint:** `PUT /customers/{id}/update/`

**Description:** Replace all customer information (all fields required).

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | Customer ID |

**Request Body:**
```json
{
  "name": "John Smith",
  "email": "john.smith@example.com",
  "date_of_birth": "1990-01-01",
  "national_id_number": "1234567890"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Smith",
  "email": "john.smith@example.com",
  "date_of_birth": "1990-01-01",
  "national_id_number": "1234567890",
  "phone_numbers": [],
  "addresses": [],
  "documents": [],
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-02T15:30:00Z"
}
```

---

### 6. Delete Customer

**Endpoint:** `DELETE /customers/{id}/delete/`

**Description:** Delete a customer and all associated phone numbers, addresses, and documents.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | Customer ID |

**Response (204 No Content):**
```
(No response body)
```

**Warning:** This action cannot be undone and will delete all related data.

**Example Request:**
```bash
DELETE /api/customers/1/delete/
```

---

## Phone Number Endpoints

### 1. List Phone Numbers for a Customer

**Endpoint:** `GET /customers/{customer_id}/phone-numbers/`

**Description:** Retrieve all phone numbers for a specific customer.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |

**Response (200 OK):**
```json
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
```

---

### 2. Create Phone Number for a Customer

**Endpoint:** `POST /customers/{customer_id}/phone-numbers/`

**Description:** Add a new phone number for a customer.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |

**Request Body:**
```json
{
  "phone_type": "PRIMARY",
  "number": "+880123456789"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "phone_type": "PRIMARY",
  "number": "+880123456789"
}
```

**Phone Type Options:**
- `PRIMARY` - Primary contact number
- `ALTERNATE` - Secondary/alternate number
- `OFFICE` - Office or business number
- `HOME` - Home phone number

---

### 3. Get Phone Number Details

**Endpoint:** `GET /customers/{customer_id}/phone-numbers/{id}/`

**Description:** Retrieve details of a specific phone number.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |
| id | integer | Phone number ID |

**Response (200 OK):**
```json
{
  "id": 1,
  "phone_type": "PRIMARY",
  "number": "+880123456789"
}
```

---

### 4. Update Phone Number

**Endpoint:** `PATCH /customers/{customer_id}/phone-numbers/{id}/`

**Description:** Update a phone number (partial update).

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |
| id | integer | Phone number ID |

**Request Body:**
```json
{
  "number": "+880111222333"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "phone_type": "PRIMARY",
  "number": "+880111222333"
}
```

---

### 5. Delete Phone Number

**Endpoint:** `DELETE /customers/{customer_id}/phone-numbers/{id}/`

**Description:** Delete a phone number for a customer.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |
| id | integer | Phone number ID |

**Response (204 No Content):**
```
(No response body)
```

---

## Address Endpoints

### 1. List Addresses for a Customer

**Endpoint:** `GET /customers/{customer_id}/addresses/`

**Description:** Retrieve all addresses for a specific customer.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "address_type": "PRESENT",
    "address_line": "123 Main St",
    "city": "Dhaka",
    "district": "Dhaka",
    "postal_code": "1000",
    "country": "Bangladesh"
  },
  {
    "id": 2,
    "address_type": "PERMANENT",
    "address_line": "456 Old St",
    "city": "Chittagong",
    "district": "Chittagong",
    "postal_code": "4000",
    "country": "Bangladesh"
  }
]
```

---

### 2. Create Address for a Customer

**Endpoint:** `POST /customers/{customer_id}/addresses/`

**Description:** Add a new address for a customer.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |

**Request Body:**
```json
{
  "address_type": "PRESENT",
  "address_line": "123 Main St",
  "city": "Dhaka",
  "district": "Dhaka",
  "postal_code": "1000",
  "country": "Bangladesh"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "address_type": "PRESENT",
  "address_line": "123 Main St",
  "city": "Dhaka",
  "district": "Dhaka",
  "postal_code": "1000",
  "country": "Bangladesh"
}
```

**Address Type Options:**
- `PRESENT` - Current residential address
- `PERMANENT` - Permanent address
- `MAILING` - Mailing address for correspondence
- `OFFICE` - Office or business address

**Required Fields:**
- `address_type`
- `address_line`
- `city`
- `district`
- `postal_code`
- `country` (defaults to "Bangladesh")

---

### 3. Get Address Details

**Endpoint:** `GET /customers/{customer_id}/addresses/{id}/`

**Description:** Retrieve details of a specific address.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |
| id | integer | Address ID |

**Response (200 OK):**
```json
{
  "id": 1,
  "address_type": "PRESENT",
  "address_line": "123 Main St",
  "city": "Dhaka",
  "district": "Dhaka",
  "postal_code": "1000",
  "country": "Bangladesh"
}
```

---

### 4. Update Address

**Endpoint:** `PATCH /customers/{customer_id}/addresses/{id}/`

**Description:** Update an address (partial update).

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |
| id | integer | Address ID |

**Request Body:**
```json
{
  "address_line": "456 New St",
  "city": "Chittagong"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "address_type": "PRESENT",
  "address_line": "456 New St",
  "city": "Chittagong",
  "district": "Dhaka",
  "postal_code": "1000",
  "country": "Bangladesh"
}
```

---

### 5. Delete Address

**Endpoint:** `DELETE /customers/{customer_id}/addresses/{id}/`

**Description:** Delete an address for a customer.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |
| id | integer | Address ID |

**Response (204 No Content):**
```
(No response body)
```

---

## Document Endpoints

### 1. List Documents for a Customer

**Endpoint:** `GET /customers/{customer_id}/documents/`

**Description:** Retrieve all documents for a specific customer.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "document_type": "NID",
    "file": "/media/customer_documents/nid_001.pdf",
    "uploaded_at": "2024-01-01T10:00:00Z"
  },
  {
    "id": 2,
    "document_type": "PHOTO",
    "file": "/media/customer_documents/photo_001.jpg",
    "uploaded_at": "2024-01-02T11:00:00Z"
  }
]
```

---

### 2. Upload Document for a Customer

**Endpoint:** `POST /customers/{customer_id}/documents/`

**Description:** Upload a new document file for a customer.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |

**Request Body (multipart/form-data):**
```
Content-Type: multipart/form-data

document_type: NID
file: <binary file content>
```

**Response (201 Created):**
```json
{
  "id": 1,
  "document_type": "NID",
  "file": "/media/customer_documents/nid_001.pdf",
  "uploaded_at": "2024-01-01T10:00:00Z"
}
```

**Document Type Options:**
- `NID` - National ID card or identification document
- `TAX_CERTIFICATE` - Tax-related certificate
- `PHOTO` - Profile photo or photograph
- `SIGNATURE` - Digital signature or signature scan

**Required Fields:**
- `document_type`
- `file` (the actual file to upload)

**Important Notes:**
- Content-Type must be `multipart/form-data`
- Files are stored in `media/customer_documents/` directory
- `uploaded_at` is automatically set to the current timestamp

**Example Request (cURL):**
```bash
curl -X POST \
  http://localhost:8000/api/customers/1/documents/ \
  -F "document_type=NID" \
  -F "file=@/path/to/nid.pdf"
```

---

### 3. Get Document Details

**Endpoint:** `GET /customers/{customer_id}/documents/{id}/`

**Description:** Retrieve details of a specific document.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |
| id | integer | Document ID |

**Response (200 OK):**
```json
{
  "id": 1,
  "document_type": "NID",
  "file": "/media/customer_documents/nid_001.pdf",
  "uploaded_at": "2024-01-01T10:00:00Z"
}
```

---

### 4. Update Document

**Endpoint:** `PATCH /customers/{customer_id}/documents/{id}/`

**Description:** Update document information or upload a new file (partial update).

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |
| id | integer | Document ID |

**Request Body (multipart/form-data) - Example 1: Change document type only:**
```
document_type: PHOTO
```

**Request Body (multipart/form-data) - Example 2: Upload new file:**
```
file: <new binary file content>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "document_type": "PHOTO",
  "file": "/media/customer_documents/photo_new.pdf",
  "uploaded_at": "2024-01-02T12:00:00Z"
}
```

**Example Request (cURL):**
```bash
# Update document type
curl -X PATCH \
  http://localhost:8000/api/customers/1/documents/1/ \
  -F "document_type=PHOTO"

# Upload new file
curl -X PATCH \
  http://localhost:8000/api/customers/1/documents/1/ \
  -F "file=@/path/to/new_photo.jpg"
```

---

### 5. Delete Document

**Endpoint:** `DELETE /customers/{customer_id}/documents/{id}/`

**Description:** Delete a document for a customer.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| customer_id | integer | Customer ID |
| id | integer | Document ID |

**Response (204 No Content):**
```
(No response body)
```

---

## Common Error Responses

### 404 Not Found
Returned when a resource (customer, phone number, address, or document) is not found.

```json
{
  "detail": "Not found."
}
```

### 400 Bad Request
Returned when request validation fails.

```json
{
  "field_name": ["Error message"],
  "another_field": ["Error message"]
}
```

### 405 Method Not Allowed
Returned when using an HTTP method not supported by the endpoint.

```json
{
  "detail": "Method \"GET\" not allowed."
}
```

### 500 Internal Server Error
Returned when an unexpected server error occurs.

```json
{
  "detail": "Internal server error."
}
```

---

## Pagination

List endpoints support pagination with the following parameters:

| Parameter | Default | Max | Description |
|-----------|---------|-----|-------------|
| page | 1 | - | Page number to retrieve |
| page_size | 10 | 100 | Number of items per page |

**Response format for paginated endpoints:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/customers/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Usage Examples

### Create a Complete Customer Profile

```bash
# 1. Create customer
curl -X POST http://localhost:8000/api/customers/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "date_of_birth": "1990-01-01",
    "national_id_number": "1234567890"
  }'

# 2. Add phone number
curl -X POST http://localhost:8000/api/customers/1/phone-numbers/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_type": "PRIMARY",
    "number": "+880123456789"
  }'

# 3. Add address
curl -X POST http://localhost:8000/api/customers/1/addresses/ \
  -H "Content-Type: application/json" \
  -d '{
    "address_type": "PRESENT",
    "address_line": "123 Main St",
    "city": "Dhaka",
    "district": "Dhaka",
    "postal_code": "1000",
    "country": "Bangladesh"
  }'

# 4. Upload document
curl -X POST http://localhost:8000/api/customers/1/documents/ \
  -F "document_type=NID" \
  -F "file=@nid.pdf"

# 5. Retrieve complete customer profile
curl http://localhost:8000/api/customers/1/
```

---

## API Version

Current API Version: 1.0

For questions or issues, please contact the development team.
