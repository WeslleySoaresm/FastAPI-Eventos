import pytest
from fastapi.testclient import TestClient
from main import app
from router.auth_router import create_access_token
from data.db import events
from models.events import Event

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Limpa e prepara massa de teste
    events.clear()
    events.append(
        Event(
            id=10,
            title="Evento do Alice",
            date="2026-10-10",
            organizer="Alice",
            organizer_id=1,  # ID do Alice
            description="Descrição do evento",
            tags=["tech"],
            location="Auditório"
        )
    )

def test_1_bloqueio_bola_acesso_indevido_outro_usuario():
    """
    TESTE 1: Garante que o usuário Bob (id=2) NÃO consegue alterar 
    um evento pertencente à Alice (organizer_id=1). Retorna 403 Forbidden.
    """
    # Token do Bob (ID=2)
    bob_token = create_access_token(data={"sub": "bob", "user_id": 2, "role": "organizador", "scope": "events:write"})
    headers = {"Authorization": f"Bearer {bob_token}"}
    
    payload = {"title": "Tentativa de Alteração Maliciosa por Bob"}

    # Bob tenta editar o evento ID 10 da Alice
    response = client.put("/event/10", json=payload, headers=headers)
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso negado: Você não possui permissão para este recurso."

def test_2_rejeicao_payload_com_campo_extra_não_documentado():
    """
    TESTE 2: Garante que um payload contendo campos extras (não mapeados no schema)
    seja rejeitado com status 422 Unprocessable Entity devido ao extra='forbid'.
    """
    # Token da Alice (ID=1 - Dono do recurso)
    alice_token = create_access_token(data={"sub": "alice", "user_id": 1, "role": "organizador", "scope": "events:write"})
    headers = {"Authorization": f"Bearer {alice_token}"}

    # Payload contendo campo não documentado "admin_override"
    payload_com_campo_extra = {
        "title": "Novo Titulo Valido",
        "admin_override": True  # Campo extra proibido
    }

    response = client.put("/event/10", json=payload_com_campo_extra, headers=headers)

    assert response.status_code == 422
    assert "extra_forbidden" in str(response.json())