import json
from unittest import mock


def empty_cache(*args, **kwargs):
    def wrapper(func):
        return func

    return wrapper


mock.patch("fastapi_cache.decorator.cache", empty_cache).start()

import pytest
from httpx import AsyncClient

from src.api.dependencies import get_db
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


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        print("!!!OVERWRITE!!!")
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


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

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels_validated)
        await db_.rooms.add_bulk(rooms_validated)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with app.router.lifespan_context(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_data_in_base, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "test@test.com",
            "password": "Pa$$w0rd"
        }
    )
