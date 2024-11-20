from pydantic import ConfigDict
from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    model_config = ConfigDict(from_attributes=True)

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ) -> list[Hotel]:
        query = select(HotelsORM)
        if location:
            query = query.filter(func.lower(HotelsORM.location)
                                 .contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsORM.title)
                                 .contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return [Hotel.model_validate(hotel, from_attributes=True)
                for hotel in result.scalars().all()]
