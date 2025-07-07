import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.auth-service.main import app, Base, get_db, DBUser

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescreve a dependência get_db para usar o banco de dados de teste
@pytest.fixture()
def session_override():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = session_override

client = TestClient(app)

def test_register_user():
    response = client.post("/register?password=testpassword", json={
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_register_user_already_exists():
    client.post("/register?password=testpassword", json={
        "username": "existinguser",
        "email": "existing@example.com",
        "full_name": "Existing User"
    })
    response = client.post("/register?password=testpassword", json={
        "username": "existinguser",
        "email": "new@example.com",
        "full_name": "New User"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

def test_login_for_access_token():
    # Primeiro, registre um usuário
    client.post("/register?password=testpassword", json={
        "username": "loginuser",
        "email": "login@example.com",
        "full_name": "Login User"
    })

    # Em seguida, tente fazer o login
    response = client.post("/token", data={"username": "loginuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post("/token", data={"username": "nonexistent", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_read_users_me():
    # Registre e faça login para obter um token
    client.post("/register?password=testpassword", json={
        "username": "meuser",
        "email": "me@example.com",
        "full_name": "Me User"
    })
    token_response = client.post("/token", data={"username": "meuser", "password": "testpassword"})
    token = token_response.json()["access_token"]

    response = client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "meuser"

def test_read_users_me_invalid_token():
    response = client.get("/users/me", headers={
        "Authorization": "Bearer invalid_token"
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}