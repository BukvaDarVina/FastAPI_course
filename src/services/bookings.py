from src.api.dependencies import PaginationDep, UserIdDep
from src.exceptions import ObjectNotFoundException, RoomNotFoundException, AllRoomsAreBookedException, \
    AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingsAddRequest, BookingAdd
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(
            self,
            pagination: PaginationDep,
            user_id: int | None,
            room_id: int | None,
    ):
        per_page = pagination.per_page or 5
        return await self.db.bookings.get_all(
            user_id=user_id,
            room_id=room_id,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_my_bookings(self, user_id: UserIdDep):
        bookings = await self.db.bookings.get_filtered(user_id=user_id)
        return bookings

    async def add_booking(self, user_id: UserIdDep, booking_data: BookingsAddRequest):
        try:
            room: Room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        hotel: Hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            # create_at=datetime(datetime.timestamp(datetime.now())),
            **booking_data.dict(),
        )
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        except AllRoomsAreBookedException as ex:
            raise AllRoomsAreBookedHTTPException from ex
        await self.db.commit()
        return booking
