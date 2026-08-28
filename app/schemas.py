import datetime as dt

from pydantic import BaseModel, HttpUrl


class TargetCreate(BaseModel):
    url: HttpUrl


class TargetOut(BaseModel):
    id: str
    url: str
    current_status: str  # "up" / "down" / "unknown"
    last_checked_at: dt.datetime | None = None
    last_latency_ms: float | None = None

    class Config:
        from_attributes = True


class CheckOut(BaseModel):
    checked_at: dt.datetime
    status_code: int | None
    latency_ms: float | None
    is_up: bool
    error: str | None

    class Config:
        from_attributes = True
