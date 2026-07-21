# Error Handling Implementation Documentation

## Overview

Comprehensive error handling has been implemented to catch, log, and respond appropriately to all possible exceptions in the Customer Management API.

## Architecture

The error handling system consists of three main components:

### 1. **Custom Exceptions** (`api/exceptions.py`)

Defines custom API exceptions that inherit from DRF's APIException:

- `DuplicateEmailError` - HTTP 400 when email already exists
- `DuplicateNationalIDError` - HTTP 400 when national ID already exists
- `InvalidDateFormatError` - HTTP 400 for invalid date formats
- `FileTooLargeError` - HTTP 413 for files exceeding 10MB
- `InvalidFileTypeError` - HTTP 400 for disallowed file types
- `FileStorageError` - HTTP 507 when file storage fails
- `InvalidPaginationError` - HTTP 400 for invalid pagination params
- `DatabaseError` - HTTP 503 for database operation failures
- `InvalidInputError` - HTTP 400 for general invalid input
- `MissingRequiredFieldError` - HTTP 400 for missing required fields

### 2. **Validators** (`api/validators.py`)

Provides field-level validation functions:

```python
# Customer validation
validate_customer_name()      # 2-255 chars, letters/spaces/hyphens/apostrophes
validate_email()              # Valid email format
validate_date_of_birth()      # Past date, reasonable age (< 150 years)
validate_national_id()        # 5-50 chars alphanumeric

# Contact validation
validate_phone_number()       # 7+ digits, max 20 chars
validate_postal_code()        # 3-20 chars

# Address validation
validate_address_line()       # 5-500 chars

# File validation
validate_file_upload()        # Size ≤ 10MB, allowed extensions
```

**Allowed File Extensions:**
- PDF, JPG, JPEG, PNG, GIF, DOC, DOCX, TXT

**Maximum File Size:**
- 10 MB (10,485,760 bytes)

### 3. **Error Handlers** (`api/error_handlers.py`)

Centralized exception handler that catches and processes exceptions:

```python
custom_exception_handler(exc, context)
```

Handles:
- **Database Integrity Errors** → 400 Bad Request
- **Database Connection Errors** → 503 Service Unavailable
- **File Operation Errors** → 400/403/507 depending on error type
- **Validation Errors** → 400 Bad Request
- **Object Not Found** → 404 Not Found
- **All Unexpected Errors** → 500 Internal Server Error

## Exception Handling Flow

```
Request
   ↓
Serializer Validation (Field-level validators)
   ↓ (if valid)
View perform_create/perform_update (Database operations)
   ↓
Database Operation (Try-Except)
   ├→ IntegrityError
   ├→ OperationalError
   ├→ ValidationError
   └→ Other exceptions
   ↓
custom_exception_handler
   ↓
Response with appropriate HTTP status & error message
```

## Configuration

### Settings.py

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'api.error_handlers.custom_exception_handler',
}

LOGGING = {
    'version': 1,
    'formatters': {...},
    'handlers': {
        'console': {...},
        'file': {...},
        'error_file': {...},
    },
    'loggers': {
        'api': {
            'level': 'DEBUG',
            'handlers': ['console', 'file', 'error_file'],
        },
    },
}
```

### Logging

- **API logs** → `logs/api.log` (all levels)
- **Error logs** → `logs/errors.log` (ERROR level only)
- **Console output** → Terminal/Docker logs

## Handled Exception Types

### 1. Database Exceptions

| Exception | Cause | Response |
|-----------|-------|----------|
| `IntegrityError` | Unique constraint violation | 400 Bad Request |
| `OperationalError` | DB connection lost | 503 Service Unavailable |
| `DatabaseError` | General DB error | 503 Service Unavailable |

### 2. Validation Exceptions

| Exception | Cause | Response |
|-----------|-------|----------|
| `ValidationError` | Invalid field data | 400 Bad Request |
| Field validators | Name, email, date, ID format | 400 Bad Request |

### 3. File Upload Exceptions

| Exception | Cause | Response |
|-----------|-------|----------|
| `FileTooLargeError` | File > 10MB | 413 Payload Too Large |
| `InvalidFileTypeError` | Disallowed extension | 400 Bad Request |
| `FileNotFoundError` | File not found | 500 Internal Server Error |
| `PermissionError` | No write permission | 403 Forbidden |
| `OSError` | Disk full/unavailable | 507 Insufficient Storage |

### 4. API Exceptions

| Exception | Cause | Response |
|-----------|-------|----------|
| `Http404` | Resource not found | 404 Not Found |
| `ParseError` | Invalid JSON | 400 Bad Request |
| `MethodNotAllowed` | Wrong HTTP method | 405 Method Not Allowed |

### 5. Unexpected Exceptions

| Exception | Cause | Response |
|-----------|-------|----------|
| Any unhandled exception | Unexpected error | 500 Internal Server Error |

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
  "detail": "A customer with this email already exists."
}
```

Or for validation errors:
```json
{
  "email": ["A customer with this email already exists."],
  "national_id_number": ["A customer with this national ID already exists."]
}
```

## Example Scenarios

### Scenario 1: Duplicate Email

**Request:**
```bash
POST /api/customers/create/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "date_of_birth": "1990-01-01",
  "national_id_number": "1234567890"
}
```

**Response (400 Bad Request):**
```json
{
  "email": ["A customer with this email already exists."]
}
```

### Scenario 2: Invalid Date Format

**Request:**
```bash
POST /api/customers/create/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "date_of_birth": "01-01-1990",
  "national_id_number": "1234567890"
}
```

**Response (400 Bad Request):**
```json
{
  "date_of_birth": ["Invalid date format. Use YYYY-MM-DD format."]
}
```

### Scenario 3: Future Date of Birth

**Request:**
```bash
POST /api/customers/create/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "date_of_birth": "2025-01-01",
  "national_id_number": "1234567890"
}
```

**Response (400 Bad Request):**
```json
{
  "date_of_birth": ["Date of birth must be in the past."]
}
```

### Scenario 4: File Too Large

**Request:**
```bash
POST /api/customers/1/documents/
Content-Type: multipart/form-data

document_type: NID
file: <15MB file>
```

**Response (413 Payload Too Large):**
```json
{
  "detail": "File size exceeds maximum allowed size (10MB). Your file is 15.23MB."
}
```

### Scenario 5: Invalid File Type

**Request:**
```bash
POST /api/customers/1/documents/
Content-Type: multipart/form-data

document_type: NID
file: document.exe
```

**Response (400 Bad Request):**
```json
{
  "detail": "File type '.exe' not allowed. Allowed types: pdf, jpg, jpeg, png, gif, doc, docx, txt"
}
```

### Scenario 6: Database Error

**Response (503 Service Unavailable):**
```json
{
  "detail": "Database operation failed. Please try again later."
}
```

## Logging Examples

### api.log (All Levels)
```
DEBUG 2024-01-01 10:00:00,123 validators 12345 67890 Validating email: john@example.com
INFO 2024-01-01 10:00:01,456 views 12345 67890 Customer created: ID=1
WARNING 2024-01-01 10:00:02,789 serializers 12345 67890 Invalid email format: invalid-email
ERROR 2024-01-01 10:00:03,012 error_handlers 12345 67890 Unexpected error (TypeError): ...
```

### errors.log (Errors Only)
```
ERROR 2024-01-01 10:00:03,012 error_handlers 12345 67890 Database operational error: ...
ERROR 2024-01-01 10:00:04,345 error_handlers 12345 67890 Unexpected error (ValueError): ...
```

## Best Practices

1. **Always validate input** - Use serializer validators
2. **Log errors appropriately** - Use logger.warning/error with context
3. **Return meaningful messages** - Help users understand what went wrong
4. **Use correct HTTP status codes** - Follow REST conventions
5. **Don't expose internal errors** - Hide sensitive details from clients

## Configuration for Production

For production, update `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

LOGGING = {
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
        },
    },
    'handlers': {
        'file': {
            'filename': '/var/log/django/api.log',
            'maxBytes': 1024 * 1024 * 50,  # 50MB
        },
    },
    'loggers': {
        'api': {
            'level': 'INFO',  # Don't log DEBUG in production
        },
    },
}
```

## Testing Error Handling

### Test Duplicate Email
```bash
curl -X POST http://localhost:8000/api/customers/create/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"existing@example.com","date_of_birth":"1990-01-01","national_id_number":"123"}'
```

### Test Invalid Date
```bash
curl -X POST http://localhost:8000/api/customers/create/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","date_of_birth":"invalid","national_id_number":"123"}'
```

### Test File Upload
```bash
curl -X POST http://localhost:8000/api/customers/1/documents/ \
  -F "document_type=NID" \
  -F "file=@large_file.pdf"  # Will fail if > 10MB
```

## Summary

The error handling implementation provides:

✅ **Comprehensive coverage** - All exception types handled  
✅ **Clear error messages** - User-friendly responses  
✅ **Proper HTTP status codes** - RESTful compliance  
✅ **Logging** - Debug and error tracking  
✅ **Validation** - Field-level and business logic checks  
✅ **Security** - No sensitive data exposure  
✅ **Reliability** - Graceful degradation on failures
