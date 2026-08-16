from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from router.events import event_router
 
app = FastAPI(redoc_url="/redoc")

app.include_router(event_router, prefix="/event")


@app.get("/")
async def status_serviço():
    return "Serviço Ativo -> API de Eventos"