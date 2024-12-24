from datetime import date

from fastapi import HTTPException
from pydantic import ConfigDict
from sqlalchemy import select

from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import Booking, BookingAdd


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

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )

        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise HTTPException(500)
