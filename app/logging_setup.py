"""Простое логирование в формате JSON — чтобы удобно смотреть через
docker compose logs и парсить основные поля (level, event, target_id)."""
import json
import logging
import sys

from app.config import settings


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
        }
        # extra-поля, которые передали через logger.info(..., extra={...})
        for key in ("event", "target_id", "url", "status_code", "latency_ms", "is_up", "error"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        return json.dumps(payload, default=str)


def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=settings.log_level, handlers=[handler])
