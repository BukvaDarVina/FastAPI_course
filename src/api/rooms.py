from fastapi import APIRouter, Query, Body

from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Комнаты"])


@router.get("", description="Получение списка всех комнат отеля")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("", summary="Добавление комнаты отеля")
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {"summary": "Стандарт", "value": {
        "title": "Стандарт",
        "description": "Стандартный номер отеля. Есть кровать, телевизор и душевая кабина",
        "price": "100",
        "quantity": "10",
    }},
    "2": {"summary": "Люкс", "value": {
        "title": "Люкс",
        "description": "Люкс номер отеля. Есть кровать, телевизор, ванная и бар",
        "price": "500",
        "quantity": "5",
    }},
})
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{room_id}", summary="Полное обновление данных о комнате")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{room_id}", summary="Частичное обновление данных о комнате")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data,
                                            exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{room_id}", summary="Удаление комнаты")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}
