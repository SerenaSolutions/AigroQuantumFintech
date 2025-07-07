
import pytest
from fastapi.testclient import TestClient
from services.ai-financial-advisor-service.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Financial Advisor Service is running"}

def test_get_financial_advice():
    response = client.post(
        "/advise",
        json={
            "query": "Qual a melhor estratégia de investimento para aposentadoria?",
            "user_context": {"age": 30, "risk_tolerance": "medium"}
        }
    )
    assert response.status_code == 200
    assert "advice" in response.json()
    assert "Entendido: Qual a melhor estratégia de investimento para aposentadoria?" in response.json()["advice"]
