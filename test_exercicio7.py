import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_rate_limit_endpoint_login():
    """
    Demonstra que após atingir o limite de 5 tentativas de login por minuto,
    a API passa a responder com HTTP 429 Too Many Requests.
    """
    payload_login = {
        "username": "alice",
        "password": "senha_errada"
    }

    # Dispara 5 requisições seguidas (limite permitido)
    for _ in range(5):
        response = client.post("/auth/login", data=payload_login)
        assert response.status_code in [200, 401]

    # A 6ª requisição no mesmo minuto deve ser bloqueada pelo Rate Limiter
    response_bloqueada = client.post("/auth/login", data=payload_login)

    assert response_bloqueada.status_code == 429
    assert "Rate limit exceeded" in response_bloqueada.json().get("error", "")