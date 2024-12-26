from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.facilities import FacilitiesAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Справочник удобств")
@cache(expire=10)
async def get_all_facilities(db: DBDep, pagination: PaginationDep):
    per_page = pagination.per_page or 5
    print("Go to DB")
    return await db.facilities.get_all(
        limit=per_page, offset=per_page * (pagination.page - 1)
    )


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
    facilities = await db.facilities.add(facilities_data)
    await db.commit()
    test_task.delay()
    return {"status": "OK", "data": facilities}
