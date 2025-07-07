import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.core-banking-service.main import app, Base, get_db, DBAccount

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

def test_create_account():
    response = client.post("/accounts", json={"account_id": "acc1", "balance": 100.0})
    assert response.status_code == 200
    assert response.json()["account_id"] == "acc1"
    assert response.json()["balance"] == 100.0

def test_create_account_already_exists():
    client.post("/accounts", json={"account_id": "acc_exists", "balance": 100.0})
    response = client.post("/accounts", json={"account_id": "acc_exists", "balance": 200.0})
    assert response.status_code == 400
    assert response.json() == {"detail": "Account already exists"}

def test_get_account():
    client.post("/accounts", json={"account_id": "acc2", "balance": 200.0})
    response = client.get("/accounts/acc2")
    assert response.status_code == 200
    assert response.json()["account_id"] == "acc2"
    assert response.json()["balance"] == 200.0

def test_get_account_not_found():
    response = client.get("/accounts/nonexistent_acc")
    assert response.status_code == 404
    assert response.json() == {"detail": "Account not found"}

def test_transfer():
    client.post("/accounts", json={"account_id": "acc3", "balance": 300.0})
    client.post("/accounts", json={"account_id": "acc4", "balance": 400.0})
    response = client.post("/transfers", json={"from_account": "acc3", "to_account": "acc4", "amount": 50.0})
    assert response.status_code == 200
    assert response.json() == {"message": "Transfer successful"}

    # Verifique os saldos após a transferência
    acc3_response = client.get("/accounts/acc3")
    acc4_response = client.get("/accounts/acc4")
    assert acc3_response.json()["balance"] == 250.0
    assert acc4_response.json()["balance"] == 450.0

def test_transfer_insufficient_funds():
    client.post("/accounts", json={"account_id": "acc_low_funds", "balance": 50.0})
    client.post("/accounts", json={"account_id": "acc_target", "balance": 100.0})
    response = client.post("/transfers", json={"from_account": "acc_low_funds", "to_account": "acc_target", "amount": 100.0})
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient funds"}

def test_transfer_sender_not_found():
    client.post("/accounts", json={"account_id": "acc_target2", "balance": 100.0})
    response = client.post("/transfers", json={"from_account": "nonexistent_sender", "to_account": "acc_target2", "amount": 10.0})
    assert response.status_code == 404
    assert response.json() == {"detail": "Sender account not found"}

def test_transfer_receiver_not_found():
    client.post("/accounts", json={"account_id": "acc_sender", "balance": 100.0})
    response = client.post("/transfers", json={"from_account": "acc_sender", "to_account": "nonexistent_receiver", "amount": 10.0})
    assert response.status_code == 404
    assert response.json() == {"detail": "Receiver account not found"}