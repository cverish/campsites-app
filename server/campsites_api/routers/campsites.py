from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import UUID4

from campsites_api.services.campsites_service import (
    CampsitesService,
    get_campsites_service,
)
from campsites_api.utils.process_data import process_data
from campsites_api.dto import CampsiteDTO


router = APIRouter(prefix="/campsites")


@router.get("", response_model=List[CampsiteDTO])
async def list_campsites(
    campsites_service: CampsitesService = Depends(get_campsites_service),
    limit: Optional[int] = 25,
    offset: Optional[int] = 0,
):
    return campsites_service.list(limit, offset)


@router.post("/upload")
async def upload_campsites(
    csv_file: UploadFile,
    campsites_service: CampsitesService = Depends(get_campsites_service),
):
    campsites: List[CampsiteDTO] = process_data(csv_file)
    campsites_service.bulk_create(campsites)


@router.post("/campsite", response_model=CampsiteDTO)
async def create_campsite(
    campsite: CampsiteDTO,
    campsites_service: CampsitesService = Depends(get_campsites_service),
):
    return campsites_service.create(campsite)


@router.get("/campsite/{campsite_uuid4}", response_model=CampsiteDTO)
async def get_campsite(
    campsite_uuid4: UUID4,
    campsites_service: CampsitesService = Depends(get_campsites_service),
):
    try:
        campsite = campsites_service.get(campsite_uuid4)
        return campsite
    except:
        raise HTTPException(status_code=404, detail="Not found")


@router.patch("/campsite/{campsite_uuid4}", response_model=CampsiteDTO)
async def update_campsite(
    campsite_uuid4: UUID4,
    campsite: CampsiteDTO,
    campsites_service: CampsitesService = Depends(get_campsites_service),
):
    return campsites_service.update(campsite_uuid4, campsite)


@router.delete("/campsite/{campsite_uuid4}")
async def delete_campsite(
    campsite_uuid4: UUID4,
    campsites_service: CampsitesService = Depends(get_campsites_service),
):
    campsites_service.delete(campsite_uuid4)
