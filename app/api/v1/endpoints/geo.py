from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.i18n import get_lang_param, localize
from app.api.deps import require_admin
from app.crud import geo as geo_crud
from app.schemas.geo import CountryOut, CountryCreate, DestinationOut, DestinationCreate

router = APIRouter(tags=["Geography"])


@router.get("/countries", response_model=list[CountryOut])
def list_countries(lang: str | None = Depends(get_lang_param), db: Session = Depends(get_db)):
    countries = geo_crud.list_countries(db)
    result = []
    for c in countries:
        result.append(CountryOut(id=c.id, name=localize(c.name, lang), slug=c.slug, cover_image=c.cover_image))
    return result


@router.post("/countries", response_model=CountryOut, dependencies=[Depends(require_admin)])
def create_country(data: CountryCreate, db: Session = Depends(get_db)):
    c = geo_crud.create_country(db, data.name, data.slug, data.cover_image)
    return CountryOut(id=c.id, name=c.name, slug=c.slug, cover_image=c.cover_image)


@router.get("/destinations", response_model=list[DestinationOut])
def list_destinations(
    country_slug: str | None = None,
    lang: str | None = Depends(get_lang_param),
    db: Session = Depends(get_db),
):
    destinations = geo_crud.list_destinations(db, country_slug)
    result = []
    for d in destinations:
        result.append(
            DestinationOut(
                id=d.id,
                name=localize(d.name, lang),
                slug=d.slug,
                description=localize(d.description, lang),
                cover_image=d.cover_image,
                country_id=d.country_id,
            )
        )
    return result


@router.post("/destinations", response_model=DestinationOut, dependencies=[Depends(require_admin)])
def create_destination(data: DestinationCreate, db: Session = Depends(get_db)):
    d = geo_crud.create_destination(db, data)
    return DestinationOut(
        id=d.id, name=d.name, slug=d.slug, description=d.description,
        cover_image=d.cover_image, country_id=d.country_id,
    )
