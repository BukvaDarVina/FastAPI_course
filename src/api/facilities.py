from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.facilities import FacilitiesAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Справочник удобств")
@cache(expire=10)
async def get_all_facilities(db: DBDep, pagination: PaginationDep):
    return await FacilityService(db).get_all_facilities(pagination)


@router.post("", summary="Добавление в справочник удобств")
async def create_facilities(
    db: DBDep,
    facilities_data: FacilitiesAdd = Body(
        openapi_examples={
            "1": {"summary": "Wi-fi", "value": {"title": "Wi-fi"}},
            "2": {"summary": "Бар", "value": {"title": "Бар"}},
        }
    ),
):
    facility = await FacilityService(db).create_facilities(facilities_data)
    return {"status": "OK", "data": facility}
