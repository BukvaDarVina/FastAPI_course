import pytest


@pytest.mark.parametrize("email, password, status_code_1, status_code_2", [
    ("test1@test1.com", "Pa$$w0rd!", 200, 401),
    ("test1@test1", "Pa$$w0rd!", 422, 401),
])
async def test_full_auth_flow(
        ac,
        email,
        password,
        status_code_1,
        status_code_2,
):

    response_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )
    assert response_register.status_code == status_code_1
    if response_register.status_code > 250:
        return

    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    assert ac.cookies["access_token"]

    response_me = await ac.get("/auth/me")
    assert response_me.json()["email"] == email

    response_logout = await ac.post("/auth/logout")
    assert not ac.cookies

    response_me_2 = await ac.get("/auth/me")
    assert response_me_2.status_code == status_code_2
