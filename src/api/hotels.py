from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение списка всех отелей")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with (async_session_maker() as session):
        query = select(HotelsORM)
        if location:
            query = query.filter(func.lower(HotelsORM.location).like(f"%{location.strip().lower()}%"))
        if title:
            query = query.filter(func.lower(HotelsORM.title).like(f"%{title.strip().lower()}%"))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)

        hotels = result.scalars().all()
        return hotels


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("", summary="Добавление отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title and hotel_data.name:
                hotel["title"] = hotel_data.title
                hotel["name"] = hotel_data.name
                return hotel
    return {"status": "Error", "description": "Указаны не все параметры"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title and hotel_data.name:
                put_hotel(hotel_id=hotel_id, title=hotel_data.title, name=hotel_data.name)
            elif hotel_data.title:
                hotel["title"] = hotel_data.title
            elif hotel_data.name:
                hotel["name"] = hotel_data.name
            else:
                return {"status": "Error", "description": "Параметры не указаны"}
            return hotel
    return {"status": "Error", "description": "Параметры не указаны"}
