# Blogging Platform Backend API

## Objective
This project is a Django-based backend API developed using the Django Rest Framework (DRF) for a multi-user blogging platform. The platform supports role-based access control (RBAC), AI-assisted article generation, and tag suggestion features, providing a robust foundation for a scalable blogging system.

---

## Features

### 1. User Management & RBAC
- **Roles**:
  - **Owner**:
    - The first user who signs up becomes the Owner.
    - Can create other users and assign roles: Admin or Member.
    - Manages feature flags.
  - **Admin**:
    - Can create, edit, and delete articles.
    - Can comment on any article.
  - **Member**:
    - Can view articles.
    - Can comment on articles.

---

### 2. Articles with AI Generation
- **Article Creation**:
  - Admins can create blog articles manually.
  - If the "LLM Article Generation" feature is enabled, Admins can request automatic content generation using a language model.
- **Tag Suggestions**:
  - If the "LLM Tags Generation" feature is enabled, the system will suggest tags upon article creation or updates.

---

### 3. Comments
- All roles (Owner, Admin, Member) can post comments on articles.

---

### 4. Feature Flags
- **LLM Article Generation**: Enable/disable AI-assisted content generation.
- **LLM Tags Generation**: Enable/disable AI-assisted tag suggestions.

---

### 5. Authentication & Authorization
- Supports Basic Auth authentication method.
- Enforces role-based access control to ensure secure operations.

---

### 6. Persistence & Data Storage
- Uses **PostgreSQL** for database storage to ensure data reliability and scalability.

---

### 7. Containerization
- Provides a Docker setup to facilitate easy deployment and local development:
  - `Dockerfile`: Defines the application’s container.
  - `docker-compose.yml`: Sets up the application and database in a seamless environment.

---

### 8. Modularity & Code Quality
- Follows DRY principles and Django best practices.
- Structured for maintainability and scalability.
- Includes tests for core functionalities:
  - Role-based access control checks.
  - Article creation.
  - Feature flag management.

---

## Installation and Setup

### Prerequisites
- Python (>=3.9)
- Docker & Docker Compose
- PostgreSQL

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/poornima1904/blogging_platform
   cd blogging_platform
   ```

2. Build and run the application using Docker:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Admin Panel: `http://localhost:8000/admin`

4. Run migrations:
   ```bash
   docker exec -it <container_name> python manage.py migrate
   ```

---

## API Endpoints

### Authentication
- `POST //api/users//`: Owner/User Signup/Login.

### Articles
- `GET /api/articles/`: List all articles.
- `POST /api/articles/`: Create a new article (Admin only).
- `PUT /api/articles/<id>/`: Update an article (Admin only).
- `DELETE /api/articles/<id>/`: Delete an article (Admin only).

### Comments
- `GET /api/comments/`: List comments on an article.
- `POST /api/comments/`: Add a comment to an article.

### Feature Flags
- `POST /api/feature-flags/`: Update feature flag status (Owner only).
- `GET /api/feature-flags/`: View feature flag status (Owner only).
- `PATCH /api/feature-flags/`: Update feature flag status (Owner only).


---

## Contributions
Contributions are welcome! Please follow the standard GitHub flow:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

For any issues or suggestions, please open an issue in the repository.

---

## Contact
For inquiries, please contact: singhpoornima1904@gmail.com

