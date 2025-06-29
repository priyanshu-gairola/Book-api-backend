from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# 🧪 Test 1: Home endpoint
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Book API"}

# 🧪 Test 2: Get all books
def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# 🧪 Test 3: Add a book
def test_create_book():
    payload = {
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": "Self-help",
        "quantity": 10
    }
    response = client.post("/books", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Atomic Habits"
    assert data["author"] == "James Clear"

# 🧪 Test 4: Get a single book (exists)
def test_get_book_by_title_found():
    response = client.get("/books/Atomic Habits")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Atomic Habits"

# 🧪 Test 5: Get a single book (not exists)
def test_get_book_by_title_not_found():
    response = client.get("/books/NonExistentBook")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_update_book_partial():
    # Step 1: Create a book to update
    create_payload = {
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": "Self-help",
        "quantity": 5
    }
    create_response = client.post("/books", json=create_payload)
    assert create_response.status_code == 200

    # Step 2: Prepare partial update data
    update_payload = {
        "genre": "Motivational"
    }

    # Step 3: Send PATCH request
    update_response = client.patch("/books/Atomic Habits", json=update_payload)
    assert update_response.status_code == 200  # ✅ Should now work

    # Step 4: Verify the update
    updated_book = update_response.json()
    assert updated_book["genre"] == "Motivational"
    assert updated_book["title"] == "Atomic Habits"  # unchanged

# 🧪 Test 7: Delete an existing book
def test_delete_book():
    response = client.delete("/books/Atomic Habits")
    assert response.status_code == 200
    assert response.json()["title"] == "Atomic Habits"

# 🧪 Test 8: Delete a non-existent book
def test_delete_book_not_found():
    response = client.delete("/books/NonExistentBook")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"