"""Модели БД и подключение через обычный (синхронный) SQLAlchemy."""
import datetime as dt
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from app.config import settings

Base = declarative_base()


class Target(Base):
    __tablename__ = "targets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    checks = relationship("Check", back_populates="target", cascade="all, delete-orphan")


class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    target_id = Column(String, ForeignKey("targets.id"))
    checked_at = Column(DateTime, default=dt.datetime.utcnow)
    status_code = Column(Integer, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    is_up = Column(Integer, default=0)  # 0/1, чтобы одинаково работало и на sqlite, и на postgres
    error = Column(String, nullable=True)

    target = relationship("Target", back_populates="checks")


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
