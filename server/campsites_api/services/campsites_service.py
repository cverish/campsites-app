from fastapi import Depends
from sqlalchemy.orm import Session

from campsites_api.dto.campsites import (
    CampsiteDTO,
    CampsiteFilterDTO,
    DistanceFilterDTO,
)
from campsites_api.services.abstract_service import AbstractService
from campsites_db.models import Campsite
from campsites_db.session import get_session


class CampsitesService(
    AbstractService[Campsite, CampsiteDTO, CampsiteFilterDTO, DistanceFilterDTO]
):
    def __init__(self, session: Session):
        super(CampsitesService, self).__init__(Campsite, session)


def get_campsites_service(session: Session = Depends(get_session)) -> CampsitesService:
    return CampsitesService(session)
