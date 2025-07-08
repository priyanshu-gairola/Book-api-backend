# 📚 FastAPI Backend for Book Review System

A complete backend built with **FastAPI**, **SQLite**, and **SQLAlchemy**, implementing authentication, book and review management, and JWT security. This project is ideal for learning full-stack backend development and preparing for interviews.

---

## 🚀 Features

- 🔐 JWT-based Authentication & Authorization
- 🧑‍💼 Role-based Access Control (Admin & User)
- 📚 Book CRUD operations
- ✍️ Review System (1 review per user per book)
- 💾 SQLite database with SQLAlchemy ORM
- 📄 Schema validation with Pydantic
- 📁 File uploads & static file serving
- ⚙️ Environment variable-based configuration
- 🔎 Filtering, Pagination & Sorting
- 🛡️ Secure password storage with `bcrypt`

---

## 🧱 Tech Stack

| Tool / Library     | Purpose                            |
|--------------------|-------------------------------------|
| **FastAPI**         | Web framework for APIs             |
| **SQLAlchemy**      | ORM for interacting with SQLite    |
| **Pydantic**        | Data validation and serialization  |
| **Uvicorn**         | ASGI server                        |
| **bcrypt**          | Secure password hashing            |
| **JWT (PyJWT)**     | User authentication tokens         |
| **python-dotenv**   | Manage environment variables       |

---

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
  2. Create Virtual Environment
  3. Install Dependencies
  4. Create .env File
  5. Run the app           uvicorn app.main:app --reload


🧪 API Endpoints
📘 Auth    
Method	Endpoint	Description
POST	/register	Register new user
POST	/login	Login & get JWT token
![image](https://github.com/user-attachments/assets/66af7569-bb79-4fd1-a255-9bec5957a243)


📗 Books
Method	Endpoint	Description
GET	/books/	Get list of books
POST	/books/	Add new book (admin)
PUT	/books/{id}	Update book (admin)
DELETE	/books/{id}	Delete book (admin)
![image](https://github.com/user-attachments/assets/8826fa4e-8432-41eb-930a-9926383e0618)


📙 Reviews
Method	Endpoint	Description
POST	/review/{book_id}	Submit review (user only)
GET	/review/book/{book_id}	View reviews for book
![image](https://github.com/user-attachments/assets/6f7b6e7e-1048-4cd0-b9b1-98bd80de9cf8)


🔐 Authentication & Security
Users must login to get a JWT token

Include token in headers:
Authorization: Bearer <token>

Role-based protection via dependency injection

Passwords are hashed with bcrypt

🔍 Advanced Features
Pagination via skip and limit query params #

Sorting using ?sort_by=price&order=asc #

File upload with /upload route #

Static files served via /static/ path #
