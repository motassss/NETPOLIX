from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.core.seed import run_seed
from app.routes import auth, videos
from app.routes.favoritos import router as favoritos_router
from app.routes.historial import router as historial_router
from app.routes.carrito import router as carrito_router
from app.routes.rentas import router as rentas_router
from app.models import historial, carrito, renta  # noqa: F401 — register models
from app.core.migrations import run_migrations
import os

Base.metadata.create_all(bind=engine)
run_migrations(engine)

app = FastAPI(
    title=settings.app_name,
    description="Dcoumentacion automatica de fastapi:)",
    version="1.0.0",

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rutas de páginas del frontend
@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("pages/index.html")

@app.get("/dashboard", response_class=FileResponse)
async def dashboard():
    return FileResponse("pages/dashboard.html")

@app.get("/login", response_class=FileResponse)
async def login_page():
    return FileResponse("pages/login.html")

@app.get("/registro", response_class=FileResponse)
async def registro_page():
    return FileResponse("pages/registro.html")

@app.get("/perfil", response_class=FileResponse)
async def perfil_page():
    return FileResponse("pages/perfil.html")

@app.get("/mi-lista")
async def mi_lista_page():
    return RedirectResponse(url="/dashboard", status_code=302)

@app.get("/carrito", response_class=FileResponse)
async def carrito_page():
    return FileResponse("pages/carrito.html")

@app.on_event("startup")
async def startup_event():
    from app.core.database import Base, engine
    Base.metadata.create_all(bind=engine)
    run_migrations(engine)
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

app.include_router(auth.router)
app.include_router(videos.router)
app.include_router(favoritos_router, prefix="/api")
app.include_router(historial_router, prefix="/api")
app.include_router(carrito_router, prefix="/api")
app.include_router(rentas_router, prefix="/api")
