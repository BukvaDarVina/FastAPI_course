import json

import pytest
from httpx import AsyncClient

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd


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

    async with AsyncClient(app=app, base_url="http://test") as ac:
        for hotel_data in hotels_data:
            await ac.post(
                "/hotels",
                json=hotel_data
            )


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
