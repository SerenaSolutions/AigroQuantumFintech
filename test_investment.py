
import pytest
from fastapi.testclient import TestClient
from services.investment-service.app.main import app
from unittest.mock import patch
import redis

# Mock do cliente Redis
@pytest.fixture
def mock_redis_client():
    with patch('services.investment-service.app.main.redis_client') as mock_client:
        yield mock_client

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo ao Investment Service da AigroNovaTech"}

def test_optimize_portfolio(mock_redis_client):
    # Simula o retorno do cache Redis
    mock_redis_client.get.return_value = None
    mock_redis_client.setex.return_value = True

    response = client.post(
        "/v1/optimizePortfolio",
        json={
            "assets": ["A", "B", "C"],
            "expected_returns": [0.1, 0.2, 0.15],
            "covariances": [[0.01, 0.005, 0.002], [0.005, 0.04, 0.01], [0.002, 0.01, 0.02]],
            "budget": 2,
            "risk_factor": 0.5
        }
    )
    assert response.status_code == 200
    assert "optimal_allocation" in response.json()
    assert "backend_used" in response.json()

def test_run_risk_simulation(mock_redis_client):
    # Simula o retorno do cache Redis
    mock_redis_client.get.return_value = None
    mock_redis_client.setex.return_value = True

    response = client.post(
        "/v1/runRiskSimulation",
        json={
            "portfolio_value": 1000000,
            "expected_return": 0.05,
            "volatility": 0.2,
            "time_horizon_days": 252,
            "num_simulations": 100
        }
    )
    assert response.status_code == 200
    assert "value_at_risk_95_percent_quantum_estimate" in response.json()

def test_get_quantum_resistant_signature():
    response = client.post(
        "/v1/getQuantumResistantSignature",
        json={"data_to_sign": "test data"}
    )
    assert response.status_code == 200
    assert "public_key" in response.json()
    assert "signature" in response.json()
