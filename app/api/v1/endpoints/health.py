from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import redis

from app.database import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {type(e).__name__}: {e}"
        )

    try:
        # Check Redis connection
        r = redis.from_url(settings.REDIS_BROKER_URL)
        r.ping()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Redis connection failed: {type(e).__name__}: {e}"
        )

    # Note: Mistral AI client doesn't have a direct "ping" method.
    # Its health is usually verified during actual API calls.
    # For a more thorough health check, one might attempt a lightweight call.

    return {"status": "ok", "message": "All services are healthy"}
