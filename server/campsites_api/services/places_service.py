from typing import Optional
from fastapi import Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from campsites_api.dto.places import PlaceDTO, PlaceFilterDTO
from campsites_api.services.abstract_service import AbstractService
from campsites_db.models import GeographicalName
from campsites_db.session import get_session


class PlacesService(AbstractService[GeographicalName, PlaceDTO, PlaceFilterDTO]):
    def __init__(self, session: Session):
        super(PlacesService, self).__init__(GeographicalName, session)

    def get(self, id: UUID4) -> GeographicalName:
        item: Optional[GeographicalName] = (
            self.session.query(self.model).filter_by(id=id).first()
        )
        if item is None:
            self.session.rollback()
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        return item


def get_places_service(session: Session = Depends(get_session)) -> PlacesService:
    return PlacesService(session)
