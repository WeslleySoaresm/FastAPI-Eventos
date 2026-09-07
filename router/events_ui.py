# --- IMPORTAÇÕES E SUAS UTILIDADES ---
import os  # Manipulação de caminhos e diretórios do sistema (essencial para localizar a pasta de templates)
from datetime import timedelta  # Gerenciamento de tempo, usado para definir a expiração do token JWT
from typing import Optional  # Declaração de tipos que podem ser opcionais ou nulos (None) em formulários

# Componentes centrais do FastAPI para rotas, formulários, exceções, requisições e códigos HTTP
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
# Classes para retornar páginas HTML renderizadas e redirecionar o navegador para outras URLs
from fastapi.responses import HTMLResponse, RedirectResponse
# Ferramenta para renderizar arquivos HTML dinâmicos usando o motor Jinja2
from fastapi.templating import Jinja2Templates
# Utilitários do SQLModel para abrir sessões de banco de dados e realizar consultas (queries)
from sqlmodel import Session, select

# Importações locais do projeto
from data.database import get_session  # Dependência injetada para abrir a sessão com o banco de dados
from models.events import Event  # Modelo de dados da tabela de eventos
from router.auth_router import (  # Funções e dados de autenticação (geração de tokens, senhas e base de usuários)
    create_access_token,
    users_db,
    verify_password,
)

# Inicialização do roteador da UI
ui_router = APIRouter(tags=["Events UI"])

# Configuração dos caminhos dinâmicos para a pasta de templates HTML
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# --- ROTAS DA INTERFACE (UI) ---

# Rota estática de Auditoria (deve vir ANTES de rotas dinâmicas como /{id})
@ui_router.get("/audit", response_class=HTMLResponse)
async def render_cia_audit(
    request: Request, session: Session = Depends(get_session)
):
  return templates.TemplateResponse(
      request=request, name="cia_audit.html", context={"request": request}
  )


# Rota para renderizar a página de listagem de todos os eventos
@ui_router.get("", response_class=HTMLResponse)
async def render_events_page(
    request: Request, session: Session = Depends(get_session)
):
  statement = select(Event)
  events_list = session.exec(statement).all()
  return templates.TemplateResponse(
      request=request, name="events.html", context={"events": events_list}
  )


# Rota para exibir o formulário de cadastro de novo evento
@ui_router.get("/new", response_class=HTMLResponse)
async def render_new_event_form(request: Request):
  return templates.TemplateResponse(request=request, name="new_event.html")


# Rota POST para processar o formulário de criação de evento
@ui_router.post("/new")
async def create_event_from_form(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    date: str = Form(...),
    organizer: str = Form(...),
    image: Optional[str] = Form(None),
    tags: Optional[str] = Form(""),
    session: Session = Depends(get_session),
):
  # Converte a string de tags separada por vírgula em uma lista Python limpa
  tags_list = (
      [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
  )

  new_event = Event(
      title=title,
      description=description,
      location=location,
      date=date,
      organizer=organizer,
      image=image,
      tags=tags_list,
  )

  session.add(new_event)
  session.commit()
  session.refresh(new_event)

  return RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)


# Rota de Login (GET para exibir a página, POST para processar as credenciais)
@ui_router.get("/login", response_class=HTMLResponse)
async def render_login_page(request: Request):
  return templates.TemplateResponse(request=request, name="login.html")


@ui_router.post("/login")
async def process_login(
    request: Request, username: str = Form(...), password: str = Form(...)
):
  user = users_db.get(username)
  if not user or not verify_password(password, user["hashed_password"]):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": "Utilizador ou palavra-passe incorretos."},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )

  access_token = create_access_token(
      data={"sub": user["username"], "user_id": user["id"]},
      expires_delta=timedelta(minutes=30),
  )

  redirect_response = RedirectResponse(
      url="/ui", status_code=status.HTTP_303_SEE_OTHER
  )
  redirect_response.set_cookie(
      key="access_token", value=f"Bearer {access_token}", httponly=True
  )
  return redirect_response


# Rota de Logout (limpa o cookie de autenticação)
@ui_router.get("/logout")
async def logout():
  redirect_response = RedirectResponse(
      url="/ui/login", status_code=status.HTTP_303_SEE_OTHER
  )
  redirect_response.delete_cookie("access_token")
  return redirect_response


# Rota para renderizar o formulário de edição de um evento específico
@ui_router.get("/edit/{id}", response_class=HTMLResponse)
async def render_edit_event_form(
    request: Request, id: int, session: Session = Depends(get_session)
):
  event_to_edit = session.get(Event, id)
  if not event_to_edit:
    raise HTTPException(status_code=404, detail="Evento não encontrado")

  return templates.TemplateResponse(
      request=request, name="edit_event.html", context={"event": event_to_edit}
  )


# Rota POST para atualizar os dados do evento vindo do formulário de edição
@ui_router.post("/edit/{id}")
async def update_event_from_form(
    id: int,
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    date: str = Form(...),
    organizer: str = Form(...),
    image: str = Form(default=""),
    tags: str = Form(default=""),
    session: Session = Depends(get_session),
):
  event_db = session.get(Event, id)
  if not event_db:
    raise HTTPException(status_code=404, detail="Evento não encontrado")

  # Trata as tags recebidas para o formato de lista JSON
  tags_list = (
      [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
  )

  event_db.title = title
  event_db.description = description
  event_db.location = location
  event_db.date = date
  event_db.organizer = organizer
  event_db.image = image
  event_db.tags = tags_list

  session.add(event_db)
  session.commit()
  session.refresh(event_db)

  return RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)


# Rota POST para excluir um evento
@ui_router.post("/delete/{id}")
async def delete_event_via_ui(id: int, session: Session = Depends(get_session)):
  event_db = session.get(Event, id)
  if event_db:
    session.delete(event_db)
    session.commit()

  return RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)


# Rota dinâmica genérica por ID (deve ficar por último para não interceptar rotas estáticas como /audit ou /new)
@ui_router.get("/{id}", response_class=HTMLResponse)
async def render_event_detail_page(
    request: Request, id: int, session: Session = Depends(get_session)
):
  event = session.get(Event, id)
  if not event:
    raise HTTPException(status_code=404, detail="Evento não encontrado")
  return templates.TemplateResponse(
      request=request, name="event_detail.html", context={"event": event}
  )