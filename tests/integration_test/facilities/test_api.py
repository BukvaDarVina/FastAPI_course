import pytest


@pytest.fixture
async def test_post_facilities(ac, setup_data_in_base):
    response = await ac.post(
        "/facilities",
        json={
            "title": "Wi-fi"
        }
    )
    print(f"{response.json()=}")

    assert response.status_code == 200


@pytest.fixture
async def test_get_facilities(ac, test_post_facilities):
    response = await ac.get("/facilities")
    print(f"{response.json()=}")

    assert response.status_code == 200
