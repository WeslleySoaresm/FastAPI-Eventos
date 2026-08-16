from typing import List

from fastapi import APIRouter, HTTPException, status
from models.events import Event
from data.db import events #Importando o db que esta em memoria
event_router = APIRouter(
    tags=["Events"]
)



# 1. Rota principal para listar todos os eventos (com validação e documentação)
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events


# 2. Rota sem response_model (deve vir antes de /{id})
@event_router.get("/not_response_model")
async def retrieve_all_events_no_model():
    return events


# 3. Rota com parâmetro dinâmico /{id}
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        # Suporta tanto objetos Pydantic quanto dicionários na lista
        event_id = event.id if isinstance(event, Event) else event.get("id")
        if event_id == id:
            return event
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


# 4. Rota para criar um novo evento com ID automático
@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(body: Event) -> dict:
    events.append({
    "id": 99,
    "title": "Evento de Teste",
    "image": "https://linktomyimage.com/image.png",
    "description": "Testando filtragem do Pydantic",
    "tags": ["teste"],
    "location": "Online",
    "internal_notes": "SENHA DO ZOOM: 123456" 
    })
    # Calcula o próximo ID de forma segura
    max_id = max((e.id if isinstance(e, Event) else e.get("id", 0) for e in events), default=0)
    body.id = max_id + 1
    
    events.append(body)
    return {
        "message": "Event created successfully"
    }