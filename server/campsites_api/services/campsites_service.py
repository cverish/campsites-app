from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from campsites_api.dto import CampsiteDTO, CampsiteFilterDTO
from campsites_api.services.abstract_service import AbstractService
from campsites_db.models import Campsite
from campsites_db.session import get_session


class CampsitesService(AbstractService[Campsite, CampsiteDTO, CampsiteFilterDTO]):
    def __init__(self, session: Session):
        super(CampsitesService, self).__init__(Campsite, session)

    # overwriting abstract create function to create 'geo' point from
    # lat and lon. The point is a string representation of the
    # Geometry Point object.
    def create(self, campsite: CampsiteDTO) -> Campsite:
        item: Campsite = self.model(
            **{**campsite.dict(), "geo": f"POINT ({campsite.lon} {campsite.lat})"}
        )
        self.session.add(item)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise HTTPException(status_code=422, detail="Item could not be created.")
        return item

    # overwriting abstract bulk_create function to create Geometry object
    def bulk_create(self, campsites: List[CampsiteDTO]) -> None:
        campsites: List[Campsite] = [
            self.model(
                **{**campsite.dict(), "geo": f"POINT ({campsite.lon} {campsite.lat})"}
            )
            for campsite in campsites
        ]
        self.session.add_all(campsites)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise HTTPException(status_code=422, detail="Items could not be created.")


def get_campsites_service(session: Session = Depends(get_session)) -> CampsitesService:
    return CampsitesService(session)
