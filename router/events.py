from typing import List

from fastapi import APIRouter, Form, HTTPException, Request, status
from models.events import Event

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.db import events #Importando o db que esta em memoria



event_router = APIRouter(
    tags=["Events"]
)

# Configura o diretório de templates Jinja2
templates = Jinja2Templates(directory="templates")

# -------------------------------------------------------------
# Rotas HTML (Interface de Usuário)
# -------------------------------------------------------------

# 1. Rota principal da UI (lista de eventos)
@event_router.get("/ui", response_class=HTMLResponse)
async def render_events_page(request: Request):
    return templates.TemplateResponse(
        "events.html", 
        {"request": request, "events": events}
    )

# 2. Rota de auditoria
@event_router.get("/ui/audit", response_class=HTMLResponse)
async def render_cia_audit_page(request: Request):
    return templates.TemplateResponse(
        "cia_audit.html",
        {"request": request}
    )   

# 3. Rota para exibir o formulário (DEVE vir ANTES de /ui/{id})
@event_router.get("/ui/new", response_class=HTMLResponse)
async def render_new_event_form(request: Request):
    return templates.TemplateResponse(
        "new_event.html",
        {"request": request}
    )

# 4. Rota POST para processar o formulário
@event_router.post("/ui/new")
async def create_event_from_form(
    title: str = Form(...),
    date: str = Form(...),
    organizer: str = Form(...),
    image: str = Form(...),
    description: str = Form(...),
    tags: str = Form(...),
    location: str = Form(...)
):
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    max_id = max((e.id if isinstance(e, Event) else e.get("id", 0) for e in events), default=0)
    
    new_event = Event(
        id=max_id + 1,
        title=title,
        date=date,
        organizer=organizer,
        image=image,
        description=description,
        tags=tag_list,
        location=location
    )
    
    events.append(new_event)
    
    return RedirectResponse(url="/event/ui", status_code=status.HTTP_303_SEE_OTHER)

# 5. Rota detalhe por ID (DEVE vir DEPOIS de rotas estáticas como /ui/new)
@event_router.get("/ui/{id}", response_class=HTMLResponse)
async def render_event_detail(request: Request, id: int):
    for event in events:
        event_id = event.id if isinstance(event, Event) else event.get("id")
        if event_id == id:
            return templates.TemplateResponse(
                "event_detail.html", 
                {"request": request, "event": event}
            )
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event not found"
    )


# -------------------------------------------------------------
# Rotas JSON (API REST)
# -------------------------------------------------------------

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events


@event_router.get("/not_response_model")
async def retrieve_all_events_no_model():
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        event_id = event.id if isinstance(event, Event) else event.get("id")
        if event_id == id:
            return event
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(body: Event) -> dict:
    max_id = max((e.id if isinstance(e, Event) else e.get("id", 0) for e in events), default=0)
    body.id = max_id + 1
    
    events.append(body)
    return {
        "message": "Event created successfully"
    }