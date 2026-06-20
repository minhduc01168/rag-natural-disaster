import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    if engine.name == "sqlite":
        # Remove SpatialFeature from metadata to prevent CompileError
        if "spatial_features" in Base.metadata.tables:
            Base.metadata.remove(Base.metadata.tables["spatial_features"])
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User",
            "phone": "0987654321",
            "location": "Hà Nội"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert data["role"] == "USER"
    assert "id" in data

def test_register_duplicate_user():
    user_data = {
        "email": "test2@example.com",
        "password": "testpassword",
        "full_name": "Test User 2"
    }
    # First registration
    client.post("/api/v1/auth/register", json=user_data)
    
    # Second registration should fail
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_login_user():
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "loginpassword",
            "full_name": "Login User"
        }
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "login@example.com",
            "password": "loginpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_incorrect_password():
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrong@example.com",
            "password": "rightpassword",
            "full_name": "Wrong User"
        }
    )
    
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

def test_get_current_user():
    # Register and login
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "me@example.com",
            "password": "mepassword",
            "full_name": "Me User"
        }
    )
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "me@example.com", "password": "mepassword"}
    )
    token = login_response.json()["access_token"]
    
    # Get /me
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"
