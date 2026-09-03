from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from models.events import Event, EventUpdateSchema, EventPublicSchema
from data.db import events
from router.auth_router import User, get_current_user

api_router = APIRouter(tags=["Events API"])

@api_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events

@api_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        event_id = event.id if isinstance(event, Event) else event.get("id")
        if event_id == id:
            return event
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Evento não encontrado."
    )

@api_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(
    body: Event, 
    current_user: User = Depends(get_current_user)
) -> dict:
    # 1. Validação de RBAC: Participantes não podem criar eventos
    if current_user.role not in ["organizador", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Seu perfil não possui permissão para criar eventos."
        )
    
    max_id = max((e.id if isinstance(e, Event) else e.get("id", 0) for e in events), default=0)
    body.id = max_id + 1
    body.organizer_id = current_user.id
    
    events.append(body)
    return {"message": "Evento criado com sucesso", "id": body.id}

@api_router.put("/{event_id}", response_model=EventPublicSchema)
async def update_event(
    event_id: int,
    event_data: EventUpdateSchema,
    current_user: User = Depends(get_current_user)
):
    evento_encontrado = None
    index_encontrado = -1

    for idx, e in enumerate(events):
        current_id = e.id if isinstance(e, Event) else e.get("id")
        if current_id == event_id:
            evento_encontrado = e
            index_encontrado = idx
            break

    if not evento_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado."
        )
    
    organizer_id = evento_encontrado.organizer_id if isinstance(evento_encontrado, Event) else evento_encontrado.get("organizer_id")

    # 2. Validação Híbrida: Permite se for o DONO ou se for ADMIN (Bypass de RBAC)
    if organizer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Você não possui permissão para alterar este evento."
        )

    # 3. Tratamento seguro para atualização (seja objeto Pydantic ou dict)
    if isinstance(evento_encontrado, dict):
        if event_data.title is not None:
            evento_encontrado["title"] = event_data.title
        if event_data.description is not None:
            evento_encontrado["description"] = event_data.description
        if event_data.location is not None:
            evento_encontrado["location"] = event_data.location
    else:
        if event_data.title is not None:
            evento_encontrado.title = event_data.title
        if event_data.description is not None:
            evento_encontrado.description = event_data.description
        if event_data.location is not None:
            evento_encontrado.location = event_data.location

    return evento_encontrado

@api_router.delete("/{event_id}")
async def delete_event_id(
    event_id: int, 
    current_user: User = Depends(get_current_user)
):
    evento_encontrado = None
    index_encontrado = -1

    for idx, e in enumerate(events):
        current_id = e.id if isinstance(e, Event) else e.get("id")
        if current_id == event_id:
            evento_encontrado = e
            index_encontrado = idx
            break

    if not evento_encontrado:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    
    organizer_id = evento_encontrado.organizer_id if isinstance(evento_encontrado, Event) else evento_encontrado.get("organizer_id")
    
    # 2. Validação Híbrida: Permite se for o DONO ou se for ADMIN (Bypass de RBAC)
    if organizer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Você não é o dono deste evento para excluí-lo."
        )
        
    events.pop(index_encontrado)
    return {
        "mensagem": f"Evento com ID {event_id} foi excluído com sucesso",
        "evento_excluido": evento_encontrado
    }