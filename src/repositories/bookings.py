from datetime import date

from pydantic import ConfigDict
from sqlalchemy import select

from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    model_config = ConfigDict(from_attributes=True)

    async def get_all(
            self,
            user_id,
            room_id,
            limit,
            offset,
    ) -> list[Booking]:
        query = select(BookingsORM)
        if user_id:
            query = query.filter(BookingsORM.user_id == user_id)
        if room_id:
            query = query.filter(BookingsORM.room_id == room_id)
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [Booking.model_validate(booking, from_attributes=True)
                for booking in result.scalars().all()]

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsORM)
            .filter(BookingsORM.date_from == date.today())
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]

    async def add_booking(self):
        pass
