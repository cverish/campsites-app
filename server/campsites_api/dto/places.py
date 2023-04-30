from enum import Enum
from typing import Dict, List, Optional
from campsites_db.models import CampsiteCountryEnum, CampsiteStateEnum

from fastapi import Query
from pydantic import BaseModel
from pydantic.types import UUID4


class PlaceDTO(BaseModel):
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

    class Config:
        orm_mode = True


class PlaceFilterDTO(BaseModel):
    limit: Optional[int] = 25
    offset: Optional[int] = 0
    sort_by: Optional[str] = "priority_order"
    sort_dir: Optional[str] = "asc"
    state_province: Optional[List[CampsiteStateEnum]]
    country: Optional[CampsiteCountryEnum]
    name_lower__ct: Optional[str]

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
        name_lower__ct: Optional[str] = Query(None),
    ) -> Dict:
        # get the list of all arguments passed
        queries = locals()
        # remove cls argument
        queries.pop("cls")
        return queries
