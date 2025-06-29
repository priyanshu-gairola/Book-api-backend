from fastapi.testclient import TestClient
from main import app

client=TestClient(app)

def test_login_success():
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    }
    client.post("/signup", json=signup_data)

    login_data = {
        "email": "test@example.com",
        "password": "testpass"
    }
    response = client.post("/login", json=login_data)

    print("🚀", response.json())  # add this to debug

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    user_payload = {
        "username": "john2",
        "email": "john2@example.com",
        "password": "realpassword"
    }
    client.post("/signup", json=user_payload)

    login_payload = {
        "email": "john2@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/login", json=login_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_login_nonexistent_user():
    login_payload = {
        "email": "doesnotexist@example.com",
        "password": "anything"
    }
    response = client.post("/login", json=login_payload)

    assert response.status_code == 401  # ✅ not 404
    assert response.json()["detail"] == "Invalid email or password"

