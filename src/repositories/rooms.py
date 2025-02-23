from datetime import date

from pydantic import ConfigDict
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomDataMapper

    model_config = ConfigDict(from_attributes=True)

    # async def get_all(
    #         self,
    #         hotel_id: int,
    #         title: str,
    #         description: str,
    #         price: int,
    #         quantity: int,
    # ) -> list[RoomDataMapper]:
    #     query = select(RoomsORM).filter_by(hotel_id=hotel_id)
    #     if title:
    #         query = query.filter(func.lower(RoomsORM.title)
    #                              .contains(title.strip().lower()))
    #     if description:
    #         query = query.filter(func.lower(RoomsORM.description)
    #                              .contains(description.strip().lower()))
    #     if price:
    #         query = query.filter_by(price=price)
    #     if quantity:
    #         query = query.filter_by(quantity=quantity)
    #
    #     # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
    #     result = await self.session.execute(query)
    #
    #     return [RoomDataMapper.map_to_domain_entity(room) for room in result.scalars().all()]

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
        return [
            RoomDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_with_rels(self, **filter_by):
        query = select(self.model).options(joinedload(self.model.facilities)).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise RoomNotFoundException
        return RoomDataWithRelsMapper.map_to_domain_entity(model)
