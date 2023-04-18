from enum import Enum
from typing import Dict, List, Optional

from fastapi import Query
from pydantic import BaseModel
from pydantic.types import UUID4

from campsites_db.models import (
    BearingEnum,
    CampsiteCountryEnum,
    CampsiteStateEnum,
    CampsiteTypeEnum,
    ToiletTypeEnum,
)


class CampsiteDTO(BaseModel):
    id: Optional[UUID4]
    code: Optional[str]
    name: str
    state: CampsiteStateEnum
    country: CampsiteCountryEnum
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
    has_rv_hookup: Optional[bool]
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


class CampsiteListDTO(BaseModel):
    items: List[CampsiteDTO]
    num_total_results: int


class SortByEnum(str, Enum):
    code = "code"
    name = "name"
    state = "state"
    country = "country"
    campsite_type = "campsite_type"


class SortDirEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class CampsiteFilterDTO(BaseModel):
    limit: Optional[int] = 25
    offset: Optional[int] = 0
    sort_by: Optional[SortByEnum] = "name"
    sort_dir: Optional[SortDirEnum] = "asc"
    code__ct: Optional[str]
    name__ct: Optional[str]
    state: Optional[List[CampsiteStateEnum]]
    country: Optional[CampsiteCountryEnum]
    campsite_type: Optional[List[CampsiteTypeEnum]]
    month_open__lt: Optional[int]
    month_close__gt: Optional[int]
    elevation_ft__gt: Optional[int]
    elevation_ft__lt: Optional[int]
    num_campsites__gt: Optional[int]
    num_campsites__lt: Optional[int]
    nearest_town_distance__lt: Optional[float]
    # amenities
    has_rv_hookup: Optional[bool]
    has_water_hookup: Optional[bool]
    has_electric_hookup: Optional[bool]
    has_sewer_hookup: Optional[bool]
    has_sanitary_dump: Optional[bool]
    max_rv_length__gt: Optional[int]
    has_toilets: Optional[bool]
    toilet_type: Optional[List[ToiletTypeEnum]]
    has_drinking_water: Optional[bool]
    has_showers: Optional[bool]
    accepts_reservations: Optional[bool]
    accepts_pets: Optional[bool]
    low_no_fee: Optional[bool]

    # arguments are the query parameters used by FastAPI. Parsing it this way means
    # we don't need to list each query parameter in the router function
    @classmethod
    def parser(
        cls,
        limit: Optional[int] = Query(25),
        offset: Optional[int] = Query(0),
        sort_by: Optional[SortByEnum] = Query("name"),
        sort_dir: Optional[SortDirEnum] = Query("asc"),
        code__ct: Optional[str] = Query(None),
        name__ct: Optional[str] = Query(None),
        state: Optional[List[CampsiteStateEnum]] = Query(None),
        country: Optional[CampsiteCountryEnum] = Query(None),
        campsite_type: Optional[List[CampsiteTypeEnum]] = Query(None),
        month_open__lt: Optional[int] = Query(None),
        month_close__gt: Optional[int] = Query(None),
        elevation_ft__gt: Optional[int] = Query(None),
        elevation_ft__lt: Optional[int] = Query(None),
        num_campsites__gt: Optional[int] = Query(None),
        num_campsites__lt: Optional[int] = Query(None),
        nearest_town_distance__lt: Optional[float] = Query(None),
        has_rv_hookup: Optional[bool] = Query(None),
        has_water_hookup: Optional[bool] = Query(None),
        has_electric_hookup: Optional[bool] = Query(None),
        has_sewer_hookup: Optional[bool] = Query(None),
        has_sanitary_dump: Optional[bool] = Query(None),
        max_rv_length__gt: Optional[int] = Query(None),
        has_toilets: Optional[bool] = Query(None),
        toilet_type: Optional[List[ToiletTypeEnum]] = Query(None),
        has_drinking_water: Optional[bool] = Query(None),
        has_showers: Optional[bool] = Query(None),
        accepts_reservations: Optional[bool] = Query(None),
        accepts_pets: Optional[bool] = Query(None),
        low_no_fee: Optional[bool] = Query(None),
    ) -> Dict:
        # get the list of all arguments passed
        queries = locals()
        # remove cls argument
        queries.pop("cls")
        return queries
