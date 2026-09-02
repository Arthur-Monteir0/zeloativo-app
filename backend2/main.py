from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.routes.link_routes import router as link_router
from app.routes import auth_routes, medicine_routes
from app.routes.medicine_routes import router as medicine_router
from app.routes.history_routes import router as history_router
from app.routes.intake_routes import router as intake_router

security = HTTPBearer()
app = FastAPI(title="Zelo Ativo API",
    description="API para gestão de medicamentos",
    version="1.0.0")

app.include_router(auth_routes.router)
app.include_router(medicine_routes.router)
app.include_router(history_router)
app.include_router(link_router)
app.include_router(intake_router)