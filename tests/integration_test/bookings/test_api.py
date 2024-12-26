import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-12-31", "2025-01-10", 200),
        (1, "2025-01-01", "2025-01-11", 200),
        (1, "2025-01-02", "2025-01-12", 200),
        (1, "2025-01-03", "2025-01-13", 200),
        (1, "2025-01-04", "2025-01-14", 200),
        (1, "2025-01-05", "2025-01-15", 500),
        (1, "2025-01-19", "2025-01-20", 200),
    ],
)
async def test_add_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    db,
    authenticated_ac,
):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms",
    [
        (1, "2024-12-31", "2025-01-10", 1),
        (1, "2025-01-01", "2025-01-11", 2),
        (1, "2025-01-02", "2025-01-12", 3),
    ],
)
async def test_add_and_get_my_bookings(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    delete_all_bookings,
    authenticated_ac,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200

    response_my_bookings = await authenticated_ac.get("/bookings/me")
    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == booked_rooms
