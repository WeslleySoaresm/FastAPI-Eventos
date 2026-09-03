from fastapi import FastAPI
from router.events_api import api_router
from router.events_ui import ui_router
from router.auth_router import api_auth

app = FastAPI(title="Gestão de Eventos")

app.include_router(api_router, prefix="/event")
app.include_router(ui_router, prefix="/ui")
app.include_router(api_auth, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)