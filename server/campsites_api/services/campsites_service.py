from fastapi import Depends
from sqlalchemy.orm import Session

from campsites_db.models import Campsite
from campsites_api.dto import CampsiteDTO
from campsites_db.session import get_session

from campsites_api.services.abstract_service import AbstractService


class CampsitesService(AbstractService[Campsite, CampsiteDTO]):
    def __init__(self, db_session: Session):
        super(CampsitesService, self).__init__(Campsite, db_session)


def get_campsites_service(session: Session = Depends(get_session)) -> CampsitesService:
    return CampsitesService(session)
