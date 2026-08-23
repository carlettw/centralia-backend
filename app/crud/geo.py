import uuid
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.geo import Country, Destination
from app.models.tour import Tour, tour_countries


def list_countries(db: Session) -> list[tuple[Country, int]]:
    """Har bir davlat uchun faol turlar sonini ham qaytaradi."""
    query = (
        select(Country, func.count(func.distinct(Tour.id)).label("tour_count"))
        .outerjoin(tour_countries, tour_countries.c.country_id == Country.id)
        .outerjoin(Tour, (Tour.id == tour_countries.c.tour_id) & (Tour.is_active == True))  # noqa: E712
        .group_by(Country.id)
    )
    return list(db.execute(query).all())


def get_country_by_slug(db: Session, slug: str) -> Country | None:
    return db.execute(select(Country).where(Country.slug == slug)).scalar_one_or_none()


def create_country(db: Session, name: dict, slug: str, cover_image: str | None) -> Country:
    country = Country(name=name, slug=slug, cover_image=cover_image)
    db.add(country)
    db.commit()
    db.refresh(country)
    return country


def list_destinations(db: Session, country_slug: str | None = None) -> list[Destination]:
    query = select(Destination)
    if country_slug:
        query = query.join(Destination.country).where(Country.slug == country_slug)
    return list(db.execute(query).scalars())


def get_destination_by_slug(db: Session, slug: str) -> Destination | None:
    return db.execute(select(Destination).where(Destination.slug == slug)).scalar_one_or_none()


def create_destination(db: Session, data) -> Destination:
    destination = Destination(**data.model_dump())
    db.add(destination)
    db.commit()
    db.refresh(destination)
    return destination
