import uuid
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.tour import TourCategory
from app.schemas.geo import CountryOut, DestinationOut


class TourImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    image_url: str
    order: int


class TourItineraryDayOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    day_number: int
    title: Any
    description: Any | None = None


class TourItineraryDayCreate(BaseModel):
    day_number: int
    title: dict
    description: dict | None = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    reviewer_name: str
    reviewer_country: str | None
    rating: int
    text: str
    images: list[str] = []
    is_verified: bool = False
    source: str | None = None
    source_url: str | None = None


class ReviewCreate(BaseModel):
    tour_id: uuid.UUID
    rating: int = Field(default=5, ge=1, le=5)
    text: str = Field(min_length=3, max_length=3000)
    images: list[str] = Field(default_factory=list, max_length=10)
    reviewer_country: str | None = None


class TourListItem(BaseModel):
    """Tour ro'yxati (kartochka) uchun yengil sxema."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: Any
    slug: str
    category: TourCategory
    duration_days: int
    duration_nights: int
    price: Decimal
    currency: str
    cover_image: str | None
    is_featured: bool = False
    countries: list[CountryOut] = []


class TourDetail(TourListItem):
    short_description: Any | None = None
    description: Any | None = None
    max_group_size: int | None = None
    destinations: list[DestinationOut] = []
    images: list[TourImageOut] = []
    itinerary: list[TourItineraryDayOut] = []
    reviews: list[ReviewOut] = []


class TourCreate(BaseModel):
    title: dict
    slug: str
    short_description: dict | None = None
    description: dict | None = None
    category: TourCategory = TourCategory.multi_day
    duration_days: int
    duration_nights: int = 0
    price: Decimal
    currency: str = "USD"
    cover_image: str | None = None
    max_group_size: int | None = None
    is_featured: bool = False
    country_ids: list[uuid.UUID] = []
    destination_ids: list[uuid.UUID] = []
    itinerary: list[TourItineraryDayCreate] = []


class TourUpdate(BaseModel):
    title: dict | None = None
    short_description: dict | None = None
    description: dict | None = None
    category: TourCategory | None = None
    duration_days: int | None = None
    duration_nights: int | None = None
    price: Decimal | None = None
    currency: str | None = None
    cover_image: str | None = None
    max_group_size: int | None = None
    is_active: bool | None = None
    is_featured: bool | None = None
    country_ids: list[uuid.UUID] | None = None
    destination_ids: list[uuid.UUID] | None = None
