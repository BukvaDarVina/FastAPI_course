from datetime import date

from pydantic import ConfigDict
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload

from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    model_config = ConfigDict(from_attributes=True)

    async def get_all(
            self,
            hotel_id: int,
            title: str,
            description: str,
            price: int,
            quantity: int,
    ) -> list[Room]:
        query = select(RoomsORM).filter_by(hotel_id=hotel_id)
        if title:
            query = query.filter(func.lower(RoomsORM.title)
                                 .contains(title.strip().lower()))
        if description:
            query = query.filter(func.lower(RoomsORM.description)
                                 .contains(description.strip().lower()))
        if price:
            query = query.filter_by(price=price)
        if quantity:
            query = query.filter_by(quantity=quantity)

        # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return [Room.model_validate(room, from_attributes=True)
                for room in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]

    async def get_one_or_none_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.unique().scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRels.model_validate(model, from_attributes=True)
