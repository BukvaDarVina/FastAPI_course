from fastapi import APIRouter, Query, Body

from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomPATCH

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Комнаты"])


@router.get("", description="Получение списка всех комнат отеля")
async def get_rooms(
        hotel_id: int,
        title: str | None = Query(default=None, description="Название комнаты"),
        description: str | None = Query(default=None, description="Описание комнаты"),
        price: int | None = Query(default=None, description="Цена комнаты"),
        quantity: int | None = Query(default=None, description="Количество комнат"),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            description=description,
            price=price,
            quantity=quantity
        )


@router.post("", summary="Добавление комнаты отеля")
async def create_room(room_data: RoomAdd = Body(openapi_examples={
    "1": {"summary": "Стандарт", "value": {
        "hotel_id": "1",
        "title": "Стандарт",
        "description": "Стандартный номер отеля. Есть кровать, телевизор и душевая кабина",
        "price": "100",
        "quantity": "10",
    }},
    "2": {"summary": "Люкс", "value": {
        "hotel_id": "1",
        "title": "Люкс",
        "description": "Люкс номер отеля. Есть кровать, телевизор, ванная и бар",
        "price": "500",
        "quantity": "5",
    }},
})
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{room_id}", summary="Полное обновление данных о комнате")
async def edit_room(room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{room_id}", summary="Частичное обновление данных о комнате")
async def patch_room(room_id: int, room_data: RoomPATCH,):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data,
                                            exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{room_id}", summary="Удаление комнаты")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}
