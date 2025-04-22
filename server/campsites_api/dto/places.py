from typing import Dict, List, Optional
from campsites_db.models import CampsiteCountryEnum, CampsiteStateEnum
from campsites_api.dto.campsites import DistanceUnitEnum, DistanceFilterDTO

from fastapi import Query
from pydantic import BaseModel, ConfigDict
from pydantic.types import UUID4


class PlaceDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    govt_id: str
    name: str
    generic_category: str
    generic_term: str
    county: Optional[str]
    state_province: CampsiteStateEnum
    country: CampsiteCountryEnum
    lat: float
    lon: float
    priority_order: int


class PlaceFilterDTO(BaseModel):
    limit: Optional[int] = 25
    offset: Optional[int] = 0
    sort_by: Optional[str] = "priority_order"
    sort_dir: Optional[str] = "asc"
    state_province: Optional[List[CampsiteStateEnum]]
    country: Optional[CampsiteCountryEnum]
    search_str__ct: Optional[str]
    distance: Optional[DistanceFilterDTO]

    # arguments are the query parameters used by FastAPI. Parsing it this way means
    # we don't need to list each query parameter in the router function
    @classmethod
    def parser(
        cls,
        limit: Optional[int] = Query(25),
        offset: Optional[int] = Query(0),
        sort_by: Optional[str] = Query("priority_order"),
        sort_dir: Optional[str] = Query("asc"),
        state_province: Optional[List[CampsiteStateEnum]] = Query(None),
        country: Optional[CampsiteCountryEnum] = Query(None),
        search_str__ct: Optional[str] = Query(None),
        distance_value: Optional[float] = Query(None),
        distance_units: Optional[DistanceUnitEnum] = Query(None),
        distance_lat: Optional[float] = Query(None),
        distance_lon: Optional[float] = Query(None),
    ) -> Dict:
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
