from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, col

from data.database import get_session
from models.events import Event, EventCreate, EventUpdateSchema, EventPublicSchema
from router.auth_router import User, check_ownership, get_current_user

api_router = APIRouter(tags=["Events API"])

@api_router.get("/search", response_model=List[EventPublicSchema])
async def search_events(
    q: str = Query(..., min_length=1, max_length=50, description="Termo de busca"),
    session: Session = Depends(get_session)
):
    statement = select(Event).where(col(Event.title).ilike(f"%{q}%"))
    return session.exec(statement).all()

@api_router.get("/", response_model=List[EventPublicSchema])
async def retrieve_all_events(session: Session = Depends(get_session)) -> List[Event]:
    statement = select(Event)
    return session.exec(statement).all()

@api_router.get("/{id}", response_model=EventPublicSchema)
async def retrieve_event(id: int, session: Session = Depends(get_session)) -> Event:
    evento = session.get(Event, id)
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    return evento

@api_router.post("/new", status_code=status.HTTP_201_CREATED, response_model=EventPublicSchema)
async def create_event(
    body: EventCreate, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role not in ["organizador", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Seu perfil não possui permissão para criar eventos."
        )
    
    novo_evento = Event.model_validate(body)
    novo_evento.organizer_id = current_user.id

    session.add(novo_evento)
    session.commit()
    session.refresh(novo_evento)

    return novo_evento

@api_router.put("/{event_id}", response_model=EventPublicSchema)
async def update_event(
    event_id: int,
    event_data: EventUpdateSchema,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    evento_db = session.get(Event, event_id)
    if not evento_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    
    if evento_db.organizer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Você não possui permissão para alterar este evento."
        )

    dados_atualizacao = event_data.model_dump(exclude_unset=True)
    for chave, valor in dados_atualizacao.items():
        setattr(evento_db, chave, valor)

    session.add(evento_db)
    session.commit()
    session.refresh(evento_db)

    return evento_db

@api_router.delete("/{event_id}")
async def delete_event_id(
    event_id: int, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    evento_db = session.get(Event, event_id)
    if not evento_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    
    check_ownership(resource_owner_id=evento_db.organizer_id, current_user=current_user)
    
    session.delete(evento_db)
    session.commit()

    return {"mensagem": f"Evento com ID {event_id} foi excluído com sucesso"}