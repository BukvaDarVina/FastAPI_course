import json

import pytest
from httpx import AsyncClient

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def setup_data_in_base(setup_database):
    with open('tests/mock_hotels.json', 'r', encoding='utf-8') as file:
        hotels_data = json.load(file)

    with open('tests/mock_rooms.json', 'r', encoding='utf-8') as file:
        rooms_data = json.load(file)

    hotels_validated = [HotelAdd.model_validate(hotel) for hotel in hotels_data]
    rooms_validated = [RoomAdd.model_validate(room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels_validated)
        await db.rooms.add_bulk(rooms_validated)
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_data_in_base):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "test@test.com",
                "password": "Pa$$w0rd"
            }
        )
