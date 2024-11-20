from fastapi import Query, APIRouter, Body

from src.repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение списка всех отелей")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Адрес отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.get("/{hotel_id}", summary="Получение отеля по id")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("", summary="Добавление отеля")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Rich 5 звезд у моря",
        "location": "г. Сочи, ул. Моря, д. 1",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Lathery 3 звезды у рынка",
        "location": "г. Дубай, ул. Шейха, д. 3",
    }},
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data,
                                             exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
