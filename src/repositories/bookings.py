from pydantic import ConfigDict
from sqlalchemy import select

from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking

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
