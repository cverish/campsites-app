from enum import Enum
from typing import Dict, List, Optional

from fastapi import Query
from pydantic import BaseModel, ConfigDict
from pydantic.types import UUID4

from campsites_db.models import (
    BearingEnum,
    CampsiteCountryEnum,
    CampsiteStateEnum,
    CampsiteTypeEnum,
    ToiletTypeEnum,
)


class CampsiteDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[UUID4] = None
    code: Optional[str] = None
    name: str
    state: CampsiteStateEnum
    country: CampsiteCountryEnum
    campsite_type: Optional[CampsiteTypeEnum] = None
    lon: float
    lat: float
    composite: str
    comments: Optional[str] = None
    phone: Optional[str] = None
    month_open: Optional[int] = None
    month_close: Optional[int] = None
    elevation_ft: Optional[int] = None
    num_campsites: Optional[int] = None
    nearest_town: Optional[str] = None
    nearest_town_distance: Optional[float] = None
    nearest_town_bearing: Optional[BearingEnum] = None
    # amenities
    has_rv_hookup: Optional[bool] = None
    has_water_hookup: Optional[bool] = None
    has_electric_hookup: Optional[bool] = None
    has_sewer_hookup: Optional[bool] = None
    has_sanitary_dump: Optional[bool] = None
    max_rv_length: Optional[int] = None
    has_toilets: Optional[bool] = None
    toilet_type: Optional[ToiletTypeEnum] = None
    has_drinking_water: Optional[bool] = None
    has_showers: Optional[bool] = None
    accepts_reservations: Optional[bool] = None
    accepts_pets: Optional[bool] = None
    low_no_fee: Optional[bool] = None


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


class DistanceUnitEnum(str, Enum):
    mi = "mi"
    km = "km"


class DistanceFilterDTO(BaseModel):
    value: Optional[int]
    units: Optional[DistanceUnitEnum]
    lat: Optional[float]
    lon: Optional[float]


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
    # distance
    distance: Optional[DistanceFilterDTO]

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
        # amenities
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
        # distance
        distance_value: Optional[float] = Query(None),
        distance_units: Optional[DistanceUnitEnum] = Query(None),
        distance_lat: Optional[float] = Query(None),
        distance_lon: Optional[float] = Query(None),
    ) -> Dict:
        # get the list of all arguments passed
        queries = locals()
        # remove cls and distance arguments
        args_to_pop = [
            "cls",
            "distance_value",
            "distance_units",
            "distance_lat",
            "distance_lon",
        ]
        for arg in args_to_pop:
            queries.pop(arg)
        # build distance filter object if all 4 included
        distance = None
        if distance_value and distance_units and distance_lat and distance_lon:
            distance = DistanceFilterDTO(
                value=distance_value,
                units=distance_units,
                lat=distance_lat,
                lon=distance_lon,
            )
        return {**queries, "distance": distance}
