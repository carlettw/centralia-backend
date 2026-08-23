from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.core.database import get_db
from app.api.deps import require_admin
from app.models.site_stats import SiteStats

router = APIRouter(prefix="/site-stats", tags=["Site Stats"])


class SiteStatsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    years_experience: int
    satisfaction_percent: int
    completed_trips: int
    happy_travelers: int


class SiteStatsUpdate(BaseModel):
    years_experience: int | None = None
    satisfaction_percent: int | None = None
    completed_trips: int | None = None
    happy_travelers: int | None = None


def _get_or_create(db: Session) -> SiteStats:
    stats = db.execute(select(SiteStats)).scalar_one_or_none()
    if not stats:
        stats = SiteStats(years_experience=0, satisfaction_percent=0, completed_trips=0, happy_travelers=0)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return stats


@router.get("", response_model=SiteStatsOut)
def get_site_stats(db: Session = Depends(get_db)):
    """Bosh sahifadagi statistika bloki uchun (login talab qilinmaydi)."""
    return _get_or_create(db)


@router.patch("", response_model=SiteStatsOut, dependencies=[Depends(require_admin)])
def update_site_stats(data: SiteStatsUpdate, db: Session = Depends(get_db)):
    """Statistika raqamlarini yangilash (faqat admin)."""
    stats = _get_or_create(db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(stats, field, value)
    db.commit()
    db.refresh(stats)
    return stats
