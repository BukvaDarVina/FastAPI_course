from fastapi import APIRouter, Query

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.schemas.bookings import BookingAdd, BookingsAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение всех бронирований в системе")
async def get_all_bookings(
    db: DBDep,
    pagination: PaginationDep,
    user_id: int | None = Query(default=None, description="ID пользователя"),
    room_id: int | None = Query(default=None, description="ID отеля")
):
    per_page = pagination.per_page or 5
    return await db.bookings.get_all(
        user_id=user_id,
        room_id=room_id,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/me", summary="Получение бронирований пользователя")
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return bookings


@router.post("", summary="Создание бронирования")
async def add_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingsAddRequest):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
