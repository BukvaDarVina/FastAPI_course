
async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2024-12-31",
            "date_to": "2025-01-01",
        }
    )
    print(f"{response.json()=}")

    assert response.status_code == 200
