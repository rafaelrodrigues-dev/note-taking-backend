# Note-Taking Backend API

This is a Django-based REST API for a note-taking application. It allows users to register, authenticate, and manage their personal notes. The API is built using Django REST Framework (DRF) and supports token-based authentication.

## Features

- User registration and authentication
- CRUD operations for notes
- Token-based authentication
- Pagination for note listings
- Docker containerization for easy deployment

## Technologies Used

- **Django**: Web framework
- **Django REST Framework**: For building REST APIs
- **PostgreSQL**: Database
- **Gunicorn**: WSGI server for production
- **Docker**: Containerization
- **Docker Compose**: Orchestration

## Setup and Installation

### Prerequisites

- Docker and Docker Compose installed on your system

### Running the Application

1. Clone the repository:
   ```
   git clone <repository-url>
   cd note-taking-api
   ```

2. Create environment files in `dotenv_files/`:
   - `.env` with database and secret key configurations

3. For development:
   ```
   docker-compose up --build
   ```

4. For production:
   ```
   docker-compose -f docker-compose-prod.yml up --build
   ```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Authentication

- **POST /api-token-auth/**: Obtain authentication token
  - Body: `{"username": "string", "password": "string"}`
  - Returns: `{"token": "string"}`

### Accounts

- **POST /api/accounts/register/**: Register a new user
  - Body: `{"username": "string", "email": "string", "password": "string"}`
  - Returns: User data

- **GET /api/accounts/{id}/**: Get user details (authenticated)
  - Headers: `Authorization: Token {token}`
  - Returns: User data

- **PATCH /api/accounts/{id}/**: Update user details (authenticated)
  - Headers: `Authorization: Token {token}`
  - Body: Partial user data
  - Returns: Updated user data

- **DELETE /api/accounts/{id}/**: Delete user (authenticated)
  - Headers: `Authorization: Token {token}`

### Notes

All note endpoints require authentication via `Authorization: Token {token}` header.

- **GET /api/notes/**: List user's notes (paginated, 10 per page)
  - Query params: `?page=1`
  - Returns: `{"count": int, "next": url, "previous": url, "results": [notes]}`

- **POST /api/notes/**: Create a new note
  - Body: `{"title": "string", "content": "string"}`
  - Returns: Created note data

- **GET /api/notes/{id}/**: Get a specific note
  - Returns: Note data

- **PATCH /api/notes/{id}/**: Update a note (partial)
  - Body: `{"title": "string"}` or `{"content": "string"}`
  - Returns: Updated note data

- **DELETE /api/notes/{id}/**: Delete a note

### Admin

- **/admin/**: Django admin interface (requires superuser credentials)

## Data Models

### User
- Standard Django User model

### Note
- `title`: CharField (max 255)
- `content`: TextField
- `created_at`: DateTimeField (auto-generated)
- `user`: ForeignKey to User

## Testing

Run tests with:
```
docker-compose exec web python manage.py test
```

## License

See LICENSE file for details.
