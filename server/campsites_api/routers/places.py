from typing import List

from fastapi import APIRouter, Depends, HTTPException

from campsites_api.dto.places import PlaceDTO, PlaceFilterDTO
from campsites_api.services.places_service import (
    PlacesService,
    get_places_service,
)
from pydantic import UUID4

router = APIRouter(prefix="/places")


@router.get("", response_model=List[PlaceDTO], tags=["GET"])
async def list_places(
    filters: PlaceFilterDTO = Depends(PlaceFilterDTO.parser),
    places_service: PlacesService = Depends(get_places_service),
):
    places, count = places_service.list(filters)
    return places


@router.get("/place/{place_uuid4}", tags=["GET"])
async def get_place(
    place_uuid4: UUID4,
    places_service: PlacesService = Depends(get_places_service),
):
    try:
        place = places_service.get(place_uuid4)
        return place
    except Exception:
        raise HTTPException(status_code=404, detail="Not found")
