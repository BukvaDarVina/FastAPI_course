

from fastapi import APIRouter, Query, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAdd, BookingsAddRequest
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение всех бронирований в системе")
@cache(expire=10)
async def get_all_bookings(
    db: DBDep,
    pagination: PaginationDep,
    user_id: int | None = Query(default=None, description="ID пользователя"),
    room_id: int | None = Query(default=None, description="ID отеля"),
):
    per_page = pagination.per_page or 5
    return await db.bookings.get_all(
        user_id=user_id,
        room_id=room_id,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get("/me", summary="Получение бронирований пользователя")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return bookings


@router.post("", summary="Создание бронирования")
async def add_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingsAddRequest):
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        # create_at=datetime(datetime.timestamp(datetime.now())),
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()

    return {"status": "OK", "data": booking}
