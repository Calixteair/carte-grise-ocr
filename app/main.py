from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import router as api_router # Renamed import
from app.database import Base, engine

app = FastAPI(
    title="Carte Grise OCR API",
    version="1.0.0",
    description="API for extracting information from car registration documents."
)

app.include_router(api_router, prefix="/api/v1")

# Create database tables (for initial setup, Alembic will handle migrations later)
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
