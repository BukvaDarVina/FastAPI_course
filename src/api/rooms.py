from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import ObjectNotFoundException, RoomNotFoundHTTPException, \
    HotelNotFoundHTTPException, HotelNotFoundException
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Комнаты"])


@router.get("", summary="Получение списка всех комнат отеля")
@cache(expire=10)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-12-01"),
    date_to: date = Query(example="2024-12-20"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{room_id}", summary="Получение информации о комнате")
@cache(expire=10)
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await db.rooms.get_one_with_rels(hotel_id=hotel_id, id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("", summary="Добавление комнаты отеля")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Стандарт",
                "value": {
                    "title": "Стандарт",
                    "description": "Стандартный номер отеля. Есть кровать, телевизор и душевая кабина",
                    "price": "100",
                    "quantity": "10",
                    "facilities_ids": [1],
                },
            },
            "2": {
                "summary": "Люкс",
                "value": {
                    "title": "Люкс",
                    "description": "Люкс номер отеля. Есть кровать, телевизор, ванная и бар",
                    "price": "500",
                    "quantity": "5",
                    "facilities_ids": [1, 2],
                },
            },
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{room_id}", summary="Полное обновление данных о комнате")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch("/{room_id}", summary="Частичное обновление данных о комнате")
async def patch_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    await RoomService(db).patch_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete("/{room_id}", summary="Удаление комнаты")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "OK"}
