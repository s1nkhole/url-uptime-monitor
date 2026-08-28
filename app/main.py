"""URL Uptime Monitor — точка входа приложения."""
import threading

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.config import settings
from app.db import init_db
from app.handlers import health, targets
from app.logging_setup import configure_logging
from app.worker.poller import run_forever

configure_logging()

app = FastAPI(title="URL Uptime Monitor", version="0.1.0")

app.include_router(targets.router)
app.include_router(health.router)


@app.on_event("startup")
def on_startup():
    init_db()
    # Поллер крутится в фоновом потоке, отдельно от основного потока FastAPI
    thread = threading.Thread(target=run_forever, daemon=True)
    thread.start()


@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port)
