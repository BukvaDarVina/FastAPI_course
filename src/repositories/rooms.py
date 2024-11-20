from pydantic import ConfigDict
from sqlalchemy import select, func

from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


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
