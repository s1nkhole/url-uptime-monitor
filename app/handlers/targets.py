import datetime as dt
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import Check, Target, get_db
from app.schemas import CheckOut, TargetCreate, TargetOut

log = logging.getLogger("url_uptime_monitor.targets")
router = APIRouter(tags=["targets"])


@router.post("/targets", response_model=TargetOut, status_code=201)
def create_target(payload: TargetCreate, db: Session = Depends(get_db)):
    url = str(payload.url)
    existing = db.query(Target).filter(Target.url == url).first()
    if existing:
        raise HTTPException(409, "target with this URL already exists")

    target = Target(url=url)
    db.add(target)
    db.commit()
    db.refresh(target)

    log.info(
        "target created",
        extra={"event": "target_created", "target_id": target.id, "url": url},
    )
    return _to_target_out(target, last_check=None)


@router.get("/targets", response_model=list[TargetOut])
def list_targets(db: Session = Depends(get_db)):
    targets = db.query(Target).all()
    result = []
    for t in targets:
        last_check = (
            db.query(Check)
            .filter(Check.target_id == t.id)
            .order_by(Check.checked_at.desc())
            .first()
        )
        result.append(_to_target_out(t, last_check))
    return result


@router.get("/targets/{target_id}/history", response_model=list[CheckOut])
def target_history(target_id: str, since_minutes: int = 60, db: Session = Depends(get_db)):
    target = db.query(Target).filter(Target.id == target_id).first()
    if not target:
        raise HTTPException(404, "target not found")

    cutoff = dt.datetime.utcnow() - dt.timedelta(minutes=since_minutes)
    checks = (
        db.query(Check)
        .filter(Check.target_id == target_id, Check.checked_at >= cutoff)
        .order_by(Check.checked_at.desc())
        .all()
    )
    return checks


def _to_target_out(target, last_check):
    status = "unknown" if last_check is None else ("up" if last_check.is_up else "down")
    return TargetOut(
        id=target.id,
        url=target.url,
        current_status=status,
        last_checked_at=last_check.checked_at if last_check else None,
        last_latency_ms=last_check.latency_ms if last_check else None,
    )
