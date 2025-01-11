

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingsAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение всех бронирований в системе")
@cache(expire=10)
async def get_all_bookings(
    db: DBDep,
    pagination: PaginationDep,
    user_id: int | None = Query(default=None, description="ID пользователя"),
    room_id: int | None = Query(default=None, description="ID отеля"),
):
    return await BookingService(db).get_all_bookings(pagination, user_id, room_id)


@router.get("/me", summary="Получение бронирований пользователя")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("", summary="Создание бронирования")
async def add_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingsAddRequest):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}
