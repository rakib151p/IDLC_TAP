# Customer Management API (IDLC_TAP)

A RESTful API for managing customer information, including personal details, contact information, addresses, and documents. Built with Django REST Framework and MySQL.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Documentation](#documentation)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The Customer Management API is a comprehensive system for managing customer data in a structured manner. It provides endpoints for CRUD operations on customers and their related information including phone numbers, addresses, and documents.

**Base URL:** `http://localhost:8000/api/`

## ✨ Features

### Core Functionality
- ✅ **Customer Management** - Create, retrieve, update, and delete customers
- ✅ **Phone Numbers** - Store multiple phone numbers per customer (primary, alternate, office, home)
- ✅ **Addresses** - Store multiple addresses per customer (present, permanent, mailing, office)
- ✅ **Documents** - Upload and manage customer documents (NID, tax certificates, photos, signatures)

### Advanced Features
- 🔍 **Search** - Search customers by name (case-insensitive)
- 📊 **Pagination** - Paginated list responses (default: 10 per page, max: 100)
- 🔄 **Ordering** - Sort customers by multiple fields (ascending/descending)
- ✔️ **Validation** - Comprehensive input validation for all fields
- 🛡️ **Error Handling** - Centralized error handling with meaningful messages
- 📝 **Logging** - Request logging and error tracking
- 📤 **File Upload** - Secure document upload (max 10MB, allowed types: PDF, JPG, PNG, GIF, DOC, DOCX, TXT)

## 🛠️ Technology Stack

- **Backend Framework:** Django 6.0.7
- **API Framework:** Django REST Framework
- **Database:** MySQL 8.0
- **Python:** 3.10+
- **Containerization:** Docker & Docker Compose
- **Task Management:** Django ORM

## 📂 Project Structure

```
IDLC_TAP/
├── config/                          # Project configuration
│   ├── __init__.py
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # URL routing
│   ├── asgi.py                     # ASGI config
│   └── wsgi.py                     # WSGI config
├── api/                             # Main API application
│   ├── migrations/                  # Database migrations
│   ├── __init__.py
│   ├── admin.py                    # Django admin configuration
│   ├── apps.py                     # App configuration
│   ├── models.py                   # Data models
│   ├── views.py                    # API views/endpoints
│   ├── serializers.py              # Data serializers
│   ├── urls.py                     # API URL routing
│   ├── exceptions.py               # Custom exceptions
│   ├── validators.py               # Field validators
│   ├── error_handlers.py           # Error handling
│   └── tests.py                    # Unit tests
├── docker-compose.yml              # Docker services
├── Dockerfile                      # Docker image
├── manage.py                       # Django management
├── requirements.txt                # Python dependencies
├── API_DOCUMENTATION.md            # Complete API documentation
├── ERROR_HANDLING.md               # Error handling documentation
├── IMPLEMENTATION_CHECKLIST.md     # Implementation details
└── README.md                       # This file
```

## 💾 Installation

### Prerequisites
- Docker & Docker Compose installed
- Python 3.10+ (for local development)
- MySQL 8.0+ (included in Docker)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/IDLC_TAP.git
cd IDLC_TAP
```

### Step 2: Create Environment File (Optional)

Create a `.env` file in the root directory for environment-specific settings:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_NAME=mydatabase
DATABASE_USER=django
DATABASE_PASSWORD=django123
DATABASE_HOST=db
DATABASE_PORT=3306
```

### Step 3: Install Dependencies (Local Development)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## ⚙️ Configuration

### Database Configuration

Update `config/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mydatabase",
        "USER": "django",
        "PASSWORD": "django123",
        "HOST": "db",  # or "localhost" for local MySQL
        "PORT": "3306",
    }
}
```

### REST Framework Configuration

Add to `config/settings.py` (if not already present):

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'api.error_handlers.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

## 🚀 Running the Application

### Using Docker Compose (Recommended)

```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The API will be available at: `http://localhost:8000/`

### Local Development (Without Docker)

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Server runs on http://localhost:8000/
```

## 📡 API Endpoints

### Customer Endpoints

```
GET     /api/customers/                      # List all customers (paginated, searchable)
POST    /api/customers/create/               # Create new customer
GET     /api/customers/<id>/                 # Get customer details
PATCH   /api/customers/<id>/update/          # Update customer (partial)
PUT     /api/customers/<id>/update/          # Update customer (full)
DELETE  /api/customers/<id>/delete/          # Delete customer
```

### Phone Number Endpoints

```
GET     /api/customers/<customer_id>/phone-numbers/             # List phone numbers
POST    /api/customers/<customer_id>/phone-numbers/             # Create phone number
GET     /api/customers/<customer_id>/phone-numbers/<id>/        # Get phone number
PATCH   /api/customers/<customer_id>/phone-numbers/<id>/        # Update phone number
DELETE  /api/customers/<customer_id>/phone-numbers/<id>/        # Delete phone number
```

### Address Endpoints

```
GET     /api/customers/<customer_id>/addresses/                 # List addresses
POST    /api/customers/<customer_id>/addresses/                 # Create address
GET     /api/customers/<customer_id>/addresses/<id>/            # Get address
PATCH   /api/customers/<customer_id>/addresses/<id>/            # Update address
DELETE  /api/customers/<customer_id>/addresses/<id>/            # Delete address
```

### Document Endpoints

```
GET     /api/customers/<customer_id>/documents/                 # List documents
POST    /api/customers/<customer_id>/documents/                 # Upload document
GET     /api/customers/<customer_id>/documents/<id>/            # Get document
PATCH   /api/customers/<customer_id>/documents/<id>/            # Update document
DELETE  /api/customers/<customer_id>/documents/<id>/            # Delete document
```

## 📚 Documentation

### Comprehensive Documentation Files

1. **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
   - Detailed endpoint descriptions
   - Request/response examples
   - Query parameters
   - Error responses
   - Pagination guide
   - Usage examples with curl commands

2. **[ERROR_HANDLING.md](ERROR_HANDLING.md)** - Error handling guide
   - Exception types and handling
   - HTTP status codes
   - Error response formats
   - Logging configuration
   - Testing error scenarios

3. **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)** - Implementation details
   - Files created and modified
   - Validation rules
   - Testing checklist
   - Configuration details

### Quick API Examples

**Create a Customer:**
```bash
curl -X POST http://localhost:8000/api/customers/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "date_of_birth": "1990-01-01",
    "national_id_number": "1234567890"
  }'
```

**List Customers (with pagination):**
```bash
curl "http://localhost:8000/api/customers/?page=1&page_size=20"
```

**Search Customers:**
```bash
curl "http://localhost:8000/api/customers/?search=john"
```

**Add Phone Number:**
```bash
curl -X POST http://localhost:8000/api/customers/1/phone-numbers/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_type": "PRIMARY",
    "number": "+880123456789"
  }'
```

**Upload Document:**
```bash
curl -X POST http://localhost:8000/api/customers/1/documents/ \
  -F "document_type=NID" \
  -F "file=@path/to/document.pdf"
```

## 🛡️ Error Handling

The API implements comprehensive error handling with:

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

Or for validation errors:

```json
{
  "field_name": ["Error message for field"]
}
```

### HTTP Status Codes

| Status Code | Meaning | Example |
|-------------|---------|---------|
| 200 | OK | Successful request |
| 201 | Created | Resource created successfully |
| 204 | No Content | Successful deletion |
| 400 | Bad Request | Invalid input, validation error |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource not found |
| 405 | Method Not Allowed | Wrong HTTP method |
| 407 | Proxy Authentication Required | Authentication required |
| 413 | Payload Too Large | File exceeds 10MB |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Database unavailable |
| 507 | Insufficient Storage | Disk space issue |

### Common Error Scenarios

**Duplicate Email:**
```json
{
  "email": ["A customer with this email already exists."]
}
```

**Invalid Date Format:**
```json
{
  "date_of_birth": ["Invalid date format. Use YYYY-MM-DD format."]
}
```

**File Too Large:**
```json
{
  "detail": "File size exceeds maximum allowed size (10MB). Your file is 15.23MB."
}
```

**Database Error:**
```json
{
  "detail": "Database operation failed. Please try again later."
}
```

See [ERROR_HANDLING.md](ERROR_HANDLING.md) for complete error handling documentation.

## ✔️ Validation Rules

### Customer Fields
- **Name**: 2-255 characters, letters/spaces/hyphens/apostrophes only
- **Email**: Valid email format, unique across system
- **Date of Birth**: YYYY-MM-DD format, must be in the past, age < 150 years
- **National ID**: 5-50 characters, alphanumeric + spaces, unique

### Contact Information
- **Phone Number**: 7+ digits, max 20 characters
- **Postal Code**: 3-20 characters

### Address Information
- **Address Line**: 5-500 characters
- **City**: 2-100 characters
- **District**: 2-100 characters

### Documents
- **Maximum File Size**: 10 MB
- **Allowed Extensions**: PDF, JPG, JPEG, PNG, GIF, DOC, DOCX, TXT
- **Document Types**: NID, TAX_CERTIFICATE, PHOTO, SIGNATURE

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test api.tests

# Run with verbose output
python manage.py test --verbosity=2
```

### Manual Testing with curl

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for comprehensive curl examples.

**Test Duplicate Email:**
```bash
curl -X POST http://localhost:8000/api/customers/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "existing@example.com",
    "date_of_birth": "1990-01-01",
    "national_id_number": "1234567890"
  }'
```

**Test Invalid Date:**
```bash
curl -X POST http://localhost:8000/api/customers/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "date_of_birth": "invalid-date",
    "national_id_number": "1234567890"
  }'
```

**Test File Upload:**
```bash
curl -X POST http://localhost:8000/api/customers/1/documents/ \
  -F "document_type=NID" \
  -F "file=@/path/to/file.pdf"
```

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## 🔧 Troubleshooting

### Database Connection Error

**Issue:** `django.db.utils.OperationalError: (2003, "Can't connect to MySQL server..."`

**Solution:**
1. Ensure MySQL is running: `docker-compose ps`
2. Check database credentials in `settings.py`
3. Wait for MySQL to start (may take 30 seconds)
4. Restart services: `docker-compose restart`

### Port Already in Use

**Issue:** `OSError: [Errno 48] Address already in use`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
# Or use different port
python manage.py runserver 8001
```

### Migration Issues

**Issue:** `django.db.migrations.exceptions.MigrationSchemaMissing`

**Solution:**
```bash
# Apply migrations
python manage.py migrate

# Create new migration if needed
python manage.py makemigrations
```

### Permission Denied on Media Upload

**Issue:** `PermissionError: [Errno 13] Permission denied`

**Solution:**
```bash
# Check media directory permissions
ls -la media/
# Set write permissions
chmod -R 755 media/
# Or in Docker
docker-compose exec web chmod -R 755 media/
```

### Logs Directory Error

**Issue:** `FileNotFoundError: [Errno 2] No such file or directory: '.../logs/api.log'`

**Solution:**
```bash
# Create logs directory
mkdir -p logs
# In Docker
docker-compose exec web mkdir -p logs
```

## 📊 Database Schema

### Customer Model
```
id (Primary Key)
name (CharField, max 255)
email (EmailField, unique)
date_of_birth (DateField)
national_id_number (CharField, max 50, unique)
created_at (DateTimeField, auto_now_add)
updated_at (DateTimeField, auto_now)
```

### PhoneNumber Model
```
id (Primary Key)
customer (ForeignKey → Customer)
phone_type (CharField - PRIMARY, ALTERNATE, OFFICE, HOME)
number (CharField, max 20)
```

### Address Model
```
id (Primary Key)
customer (ForeignKey → Customer)
address_type (CharField - PRESENT, PERMANENT, MAILING, OFFICE)
address_line (TextField)
city (CharField, max 100)
district (CharField, max 100)
postal_code (CharField, max 20)
country (CharField, max 100, default "Bangladesh")
```

### Document Model
```
id (Primary Key)
customer (ForeignKey → Customer)
document_type (CharField - NID, TAX_CERTIFICATE, PHOTO, SIGNATURE)
file (FileField, upload_to "customer_documents/")
uploaded_at (DateTimeField, auto_now_add)
```

## 📞 Support

For issues or questions:
1. Check [ERROR_HANDLING.md](ERROR_HANDLING.md) for error solutions
2. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
3. Check logs: `logs/api.log` and `logs/errors.log`
4. See Troubleshooting section above

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Django REST Framework community
- MySQL documentation
- Docker community

---

**Last Updated:** 2026-07-22  
**Version:** 1.0.0  
**Status:** Production Ready ✅
