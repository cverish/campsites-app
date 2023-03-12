from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4

from campsites_db.models import BearingEnum, CampsiteTypeEnum, ToiletTypeEnum


class CampsiteDTO(BaseModel):
    id: Optional[UUID4]
    code: Optional[str]
    name: str
    state: str
    campsite_type: Optional[CampsiteTypeEnum]
    lon: float
    lat: float
    composite: str
    comments: Optional[str]
    phone: Optional[str]
    month_open: Optional[int]
    month_close: Optional[int]
    elevation_ft: Optional[int]
    num_campsites: Optional[int]
    nearest_town: Optional[str]
    nearest_town_distance: Optional[float]
    nearest_town_bearing: Optional[BearingEnum]
    # amenities
    has_water_hookup: Optional[bool]
    has_electric_hookup: Optional[bool]
    has_sewer_hookup: Optional[bool]
    has_sanitary_dump: Optional[bool]
    max_rv_length: Optional[int]
    has_toilets: Optional[bool]
    toilet_type: Optional[ToiletTypeEnum]
    has_drinking_water: Optional[bool]
    has_showers: Optional[bool]
    accepts_reservations: Optional[bool]
    accepts_pets: Optional[bool]
    low_no_fee: Optional[bool]

    class Config:
        orm_mode = True
