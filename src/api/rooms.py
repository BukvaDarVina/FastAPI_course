from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Комнаты"])


@router.get("", summary="Получение списка всех комнат отеля")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-12-01"),
        date_to: date = Query(example="2024-12-20"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{room_id}", summary="Получение информации о комнате")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("", summary="Добавление комнаты отеля")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
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
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{room_id}", summary="Полное обновление данных о комнате")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{room_id}", summary="Частичное обновление данных о комнате")
async def patch_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{room_id}", summary="Удаление комнаты")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}
