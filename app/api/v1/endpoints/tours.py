import math
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.i18n import get_lang_param, localize
from app.api.deps import require_admin
from app.crud import tour as tour_crud
from app.models.tour import Tour, TourCategory
from app.schemas.common import Page
from app.schemas.tour import TourListItem, TourDetail, TourCreate, TourUpdate
from app.schemas.geo import CountryOut, DestinationOut

router = APIRouter(prefix="/tours", tags=["Tours"])


def _to_list_item(t: Tour, lang: str | None) -> TourListItem:
    return TourListItem(
        id=t.id, title=localize(t.title, lang), slug=t.slug, category=t.category,
        duration_days=t.duration_days, duration_nights=t.duration_nights,
        price=t.price, currency=t.currency, cover_image=t.cover_image,
        countries=[CountryOut(id=c.id, name=localize(c.name, lang), slug=c.slug, cover_image=c.cover_image) for c in t.countries],
    )


def _to_detail(t: Tour, lang: str | None) -> TourDetail:
    base = _to_list_item(t, lang)
    return TourDetail(
        **base.model_dump(),
        short_description=localize(t.short_description, lang),
        description=localize(t.description, lang),
        max_group_size=t.max_group_size,
        destinations=[
            DestinationOut(id=d.id, name=localize(d.name, lang), slug=d.slug,
                            description=localize(d.description, lang), cover_image=d.cover_image, country_id=d.country_id)
            for d in t.destinations
        ],
        images=[{"id": i.id, "image_url": i.image_url, "order": i.order} for i in sorted(t.images, key=lambda x: x.order)],
        itinerary=[
            {"id": day.id, "day_number": day.day_number, "title": localize(day.title, lang), "description": localize(day.description, lang)}
            for day in t.itinerary
        ],
        reviews=[
            {"id": r.id, "reviewer_name": r.reviewer_name, "reviewer_country": r.reviewer_country,
             "rating": r.rating, "text": r.text, "images": r.images or [], "is_verified": r.is_verified,
             "source": r.source, "source_url": r.source_url}
            for r in t.reviews if r.is_published
        ],
    )


@router.get("", response_model=Page[TourListItem])
def list_tours(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    country: str | None = None,
    destination: str | None = None,
    category: TourCategory | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    lang: str | None = Depends(get_lang_param),
    db: Session = Depends(get_db),
):
    items, total = tour_crud.list_tours(
        db, page, page_size, country, destination, category, min_price, max_price, search
    )
    return Page(
        items=[_to_list_item(t, lang) for t in items],
        total=total, page=page, page_size=page_size,
        pages=math.ceil(total / page_size) if total else 0,
    )


@router.get("/{slug}", response_model=TourDetail)
def get_tour(slug: str, lang: str | None = Depends(get_lang_param), db: Session = Depends(get_db)):
    tour = tour_crud.get_by_slug(db, slug)
    if not tour:
        raise HTTPException(status_code=404, detail="Tur topilmadi")
    return _to_detail(tour, lang)


@router.post("", response_model=TourDetail, dependencies=[Depends(require_admin)])
def create_tour(data: TourCreate, db: Session = Depends(get_db)):
    tour = tour_crud.create_tour(db, data)
    return _to_detail(tour, None)


@router.patch("/{tour_id}", response_model=TourDetail, dependencies=[Depends(require_admin)])
def update_tour(tour_id: uuid.UUID, data: TourUpdate, db: Session = Depends(get_db)):
    tour = tour_crud.get_by_id(db, tour_id)
    if not tour:
        raise HTTPException(status_code=404, detail="Tur topilmadi")
    tour = tour_crud.update_tour(db, tour, data)
    return _to_detail(tour, None)


@router.delete("/{tour_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_tour(tour_id: uuid.UUID, db: Session = Depends(get_db)):
    tour = tour_crud.get_by_id(db, tour_id)
    if not tour:
        raise HTTPException(status_code=404, detail="Tur topilmadi")
    tour_crud.delete_tour(db, tour)
