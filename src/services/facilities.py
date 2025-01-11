from src.api.dependencies import PaginationDep
from src.schemas.facilities import FacilitiesAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_all_facilities(self, pagination: PaginationDep):
        per_page = pagination.per_page or 5
        return await self.db.facilities.get_all(limit=per_page, offset=per_page * (pagination.page - 1))

    async def create_facilities(self, facilities_data: FacilitiesAdd):
        facility = await self.db.facilities.add(facilities_data)
        await self.db.commit()

        test_task.delay()  # type: ignore
        return facility
