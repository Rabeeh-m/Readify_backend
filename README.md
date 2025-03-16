# Readify Backend

This repository contains the backend for Readify, a web application for managing personal book collections and reading lists. It is built with Django REST Framework.

## Features
- User authentication with JWT
- API endpoints for books and reading lists
- File uploads for book PDFs and cover images
- Persistent storage of user data and list ordering

## Prerequisites
- **Python** (3.10 or higher)
- **Git** (for cloning the repository)

## Setup Instructions

### 1. Clone the Repository
```bash
  git clone https://github.com/<your-username>/Readify_backend.git
  cd Readify_backend
```

### 2. Create a Virtual Environment
```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
  pip install -r requirements.txt
```

### 4. Configure Environment Variables
  DEBUG=True
  SECRET_KEY=your-secret-key-here
  DATABASE_URL=sqlite:///db.sqlite3

### 5. Apply Migrations
```bash
  python manage.py makemigrations
  python manage.py migrate
```

### 6. Create a Superuser (Optional)
```bash
  python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
  python manage.py runserver
```

## API Endpoints

| Endpoint                                      | Method         | Description                   | Permissions       |
|-----------------------------------------------|----------------|-------------------------------|-------------------|
| `/api/token/`                                 | `POST`         | Obtain JWT tokens             | `AllowAny`        |
| `/api/token/refresh/`                         | `POST`         | Refresh access token          | `AllowAny`        |
| `/api/register/`                              | `POST`         | Register a new user           | `AllowAny`        |
| `/api/profile/`                               | `GET`          | Get user profile              | `IsAuthenticated` |
| `/api/profile/update/`                        | `PUT`          | Update user profile           | `IsAuthenticated` |
| `/api/books/`                                 | `GET/POST`     | List or create books          | `IsAuthenticated` |
| `/api/books/<id>/`                            | `GET`          | Get book details              | `AllowAny`        |
| `/api/books/<id>/delete/`                     | `DELETE`       | Delete a book                 | `IsAuthenticated` |
| `/api/reading-lists/`                         | `GET/POST`     | List or create reading lists  | `IsAuthenticated` |
| `/api/reading-lists/<id>/`                    | `GET/PUT/DELETE` | Manage a reading list       | `IsAuthenticated` |
| `/api/reading-lists/<id>/items/`              | `POST`         | Add book to list              | `IsAuthenticated` |
| `/api/reading-lists/<id>/items/<item_id>/`    | `DELETE`       | Remove book from list         | `IsAuthenticated` |

  For detailed endpoint documentation:
    - http://127.0.0.1:8000/api/schema/swagger-ui/
    - http://127.0.0.1:8000/api/schema/redoc/
    
## Contributing
- Fork the repository.
- Create a feature branch (git checkout -b feature-name).
- Commit changes (git commit -m "Add feature").
- Push to the branch (git push origin feature-name).
- Open a pull request.
