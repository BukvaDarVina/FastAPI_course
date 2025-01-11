from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение списка всех отелей")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Адрес отеля"),
    date_from: date = Query(example="2024-12-01"),
    date_to: date = Query(example="2024-12-20"),
):
    hotels = await HotelService(db).get_filtered_by_time(
        pagination,
        title,
        location,
        date_from,
        date_to,
    )
    return hotels


@router.get("/{hotel_id}", summary="Получение отеля по id")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", summary="Добавление отеля")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Rich 5 звезд у моря",
                    "location": "г. Сочи, ул. Моря, д. 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Lathery 3 звезды у рынка",
                    "location": "г. Дубай, ул. Шейха, д. 3",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
