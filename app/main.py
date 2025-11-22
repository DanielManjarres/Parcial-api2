from fastapi import FastAPI
from app.database import init_db
from app.controllers import router  # Asegúrate de que se llame "router"

app = FastAPI(
    title="Parcial API - Users & Tasks",
    description="API completa con pruebas unitarias, integración y E2E",
    version="1.0.0"
)

# Esto es lo que te faltaba: INCLUIR EL ROUTER
app.include_router(router)

# Esto está deprecado, pero si lo tenías, dejalo por ahora (no rompe nada)
@app.on_event("startup")
def startup():
    init_db()
    