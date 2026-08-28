"""Фоновый поток, который раз в POLL_INTERVAL_SECONDS обходит все цели
и записывает результат в БД + метрики Prometheus."""
import logging
import time

import requests
from prometheus_client import Counter, Histogram

from app.config import settings
from app.db import Check, SessionLocal, Target

log = logging.getLogger("url_uptime_monitor.worker")

checks_total = Counter(
    "healthcheck_checks_total", "Total checks performed", ["target_url", "result"]
)
check_latency_seconds = Histogram(
    "healthcheck_latency_seconds", "External check latency", ["target_url"]
)


def check_one(db, target):
    start = time.perf_counter()
    status_code = None
    error = None
    is_up = False

    try:
        resp = requests.get(target.url, timeout=settings.http_timeout_seconds)
        status_code = resp.status_code
        is_up = resp.status_code < 400
    except requests.RequestException as exc:
        error = str(exc)

    latency_ms = (time.perf_counter() - start) * 1000
    result_label = "up" if is_up else "down"

    checks_total.labels(target_url=target.url, result=result_label).inc()
    check_latency_seconds.labels(target_url=target.url).observe(latency_ms / 1000)

    log.info(
        "check completed",
        extra={
            "event": "check_completed",
            "target_id": target.id,
            "url": target.url,
            "status_code": status_code,
            "latency_ms": round(latency_ms, 1),
            "is_up": is_up,
            "error": error,
        },
    )

    db.add(Check(
        target_id=target.id,
        status_code=status_code,
        latency_ms=latency_ms,
        is_up=1 if is_up else 0,
        error=error,
    ))
    db.commit()


def run_forever():
    log.info("poller started", extra={"event": "poller_started"})
    while True:
        db = SessionLocal()
        try:
            targets = db.query(Target).all()
            for target in targets:
                check_one(db, target)
        except Exception:
            log.exception("poller iteration failed", extra={"event": "poller_error"})
        finally:
            db.close()
        time.sleep(settings.poll_interval_seconds)
