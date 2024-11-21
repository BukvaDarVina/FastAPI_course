from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingsAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Создание бронирования")
async def create_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingsAddRequest):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.session.commit()

    return {"status": "OK", "data": booking}
