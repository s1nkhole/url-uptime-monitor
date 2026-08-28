"""Настройки приложения, берутся из переменных окружения."""
import os


class Settings:
    port = int(os.getenv("APP_PORT", "8000"))
    database_url = os.getenv("DATABASE_URL", "sqlite:///./url_uptime_monitor.db")
    poll_interval_seconds = int(os.getenv("POLL_INTERVAL_SECONDS", "15"))
    http_timeout_seconds = float(os.getenv("HTTP_TIMEOUT_SECONDS", "5"))
    log_level = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
