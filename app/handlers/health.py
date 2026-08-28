from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health(db: Session = Depends(get_db)):
    """Проверка, что сервис жив и БД отвечает. Используется Docker healthcheck."""
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
