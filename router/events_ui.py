import os
from datetime import timedelta
from fastapi import APIRouter, Form, HTTPException, Path, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.events import Event
from data.db import events
from router.auth_router import verify_password, users_db, create_access_token

# Criamos um router específico para a Interface Gráfica
ui_router = APIRouter(tags=["Events UI"])

# Configura o diretório de templates Jinja2
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# 1. Rota principal da UI (lista de eventos) -> /ui
@ui_router.get("", response_class=HTMLResponse)
async def render_events_page(request: Request):
    return templates.TemplateResponse(
        "events.html", 
        {"request": request, "events": events}
    )

# 2. Rota de auditoria -> /ui/audit
@ui_router.get("/audit", response_class=HTMLResponse)
async def render_cia_audit_page(request: Request):
    return templates.TemplateResponse(
        "cia_audit.html",
        {"request": request}
    )   

# 3. Rota para exibir o formulário -> /ui/new
@ui_router.get("/new", response_class=HTMLResponse)
async def render_new_event_form(request: Request):
    return templates.TemplateResponse(
        "new_event.html",
        {"request": request}
    )

# 4. Rota POST para processar o formulário -> /ui/new
@ui_router.post("/new")
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
    
    return RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)

from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse

@ui_router.get("/logout")
async def logout(response: Response):
    # Redireciona o usuário para a tela de login limpando o cookie do token JWT
    redirect_response = RedirectResponse(url="/ui/login", status_code=303)
    redirect_response.delete_cookie("access_token")
    return redirect_response

# 5. Rota para exibir o formulário de Login -> /ui/login
@ui_router.get("/login", response_class=HTMLResponse)
async def render_login_page(request: Request):
    # CORREÇÃO AQUI: trocado Request por request
    return templates.TemplateResponse("login.html", {"request": request})

# 6. Rota para processar o formulário de Login -> /ui/login
@ui_router.post("/login")
async def process_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    # CORREÇÃO AQUI: alterado 'db' para 'users_db'
    user = users_db.get(username)
    
    # Valida o utilizador e a palavra-passe
    if not user or not verify_password(password, user["hashed_password"]):
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Utilizador ou palavra-passe incorretos."},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    # Gera o Token JWT real
    access_token = create_access_token(
        data={"sub": user["username"], "user_id": user["id"]},
        expires_delta=timedelta(minutes=30)
    )
    
    # Redireciona para a página principal guardando o Token num Cookie seguro
    redirect_response = RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)
    redirect_response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}", 
        httponly=True
    )
    return redirect_response

@ui_router.post("/edit/{id}")
async def update_event_from_form(
    id: int,
    title: str = Form(...),
    date: str = Form(...),
    organizer: str = Form(...),
    image: str = Form(...),
    description: str = Form(...),
    tags: str = Form(...),
    location: str = Form(...)
):
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]

    for idx, e in enumerate(events):
        current_id = e.id if isinstance(e, Event) else e.get("id")
        if current_id == id:
            if isinstance(e, Event):
                e.title = title
                e.date = date
                e.organizer = organizer
                e.image = image
                e.description = description
                e.tags = tag_list
                e.location = location
            else:
                events[idx] = {
                    "id": id,
                    "title": title,
                    "date": date,
                    "organizer": organizer,
                    "image": image,
                    "description": description,
                    "tags": tag_list,
                    "location": location
                }
            break

    return RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)




@ui_router.post("/delete/{id}")
async def delete_event_via_ui(id: int):
    global events
    events = [e for e in events if (e.id if isinstance(e, Event) else e.get("id")) != id]
    return RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)

@ui_router.get("/edit/{id}", response_class=HTMLResponse)
async def render_edit_event_form(request: Request, id: int):
    event_to_edit = next((e for e in events if (e.id if isinstance(e, Event) else e.get("id")) == id), None)
    if not event_to_edit:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return templates.TemplateResponse("edit_event.html", {"request": request, "event": event_to_edit})



