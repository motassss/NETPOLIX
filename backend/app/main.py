from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.routes import auth,videos

Basemetadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Dcoumentacion automatica de fastapi:)",
    version="1.0.0",

)    

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(videos.router)

@app.get("/")
def root():
    return {
        "message": "Bienvenido! :) ",
        "documentacion": "/docs",
        "version": "1.0.0"
    }
