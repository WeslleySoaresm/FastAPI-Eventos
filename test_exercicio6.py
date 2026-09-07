import pytest
from fastapi.testclient import TestClient
from main import app
import python_multipart
client = TestClient(app)

def test_1_validar_cabecalhos_de_seguranca():
    """
    Garante que todas as respostas contêm os cabeçalhos HSTS, X-Frame-Options e X-Content-Type-Options.
    """
    response = client.get("/event/")
    
    assert response.status_code == 200
    assert response.headers.get("Strict-Transport-Security") == "max-age=31536000; includeSubDomains"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-Content-Type-Options") == "nosniff"

def test_2_cors_bloqueio_origem_nao_autorizada():
    """
    Simula uma requisição preflight (OPTIONS) feita por um navegador vinda de uma origem não listada na allowlist.
    O CORS não deve retornar o cabeçalho 'Access-Control-Allow-Origin' para esta origem.
    """
    headers_origem_maliciosa = {
        "Origin": "http://site-malicioso.com",
        "Access-Control-Request-Method": "GET"
    }
    
    response = client.options("/event/", headers=headers_origem_maliciosa)
    
    # O servidor recusa conceder permissão de leitura cross-origin
    assert "Access-Control-Allow-Origin" not in response.headers

def test_3_cors_permissao_origem_autorizada():
    """
    Garante que origens presentes na allowlist recebam o cabeçalho de permissão.
    """
    headers_origem_valida = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    }
    
    response = client.options("/event/", headers=headers_origem_valida)
    
    assert response.headers.get("Access-Control-Allow-Origin") == "http://localhost:3000"