from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import UUIDPKMixin, TimestampMixin


class SiteStats(UUIDPKMixin, TimestampMixin, Base):
    """
    Bosh sahifadagi statistika bloki uchun bitta (singleton) qator.
    Masalan: '12 yillik tajriba', '95% mijozlar mamnunligi' va h.k.
    Admin panel orqali tahrirlanadi, frontend GET /site-stats bilan oladi.
    """
    __tablename__ = "site_stats"

    years_experience: Mapped[int] = mapped_column(Integer, default=0)
    satisfaction_percent: Mapped[int] = mapped_column(Integer, default=0)
    completed_trips: Mapped[int] = mapped_column(Integer, default=0)
    happy_travelers: Mapped[int] = mapped_column(Integer, default=0)
