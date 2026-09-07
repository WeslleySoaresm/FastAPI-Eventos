from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from router.events_api import api_router
from router.events_ui import ui_router
from router.auth_router import api_auth
from core.security import setup_security_middlewares

import models.users
import models.events
from data.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Garante a criação de todas as tabelas registradas no SQLModel
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Gestão de Eventos", lifespan=lifespan)

# Aplica os middlewares de segurança (Rate limit, CORS, Headers)
setup_security_middlewares(app)

# Inclui os roteadores
app.include_router(ui_router, prefix="/ui")
app.include_router(api_router, prefix="/event")
app.include_router(api_auth, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)