import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.geo import Country, Destination


def list_countries(db: Session) -> list[Country]:
    return list(db.execute(select(Country)).scalars())


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
