import pytest


@pytest.mark.parametrize(
    "email, password, status_code_1, status_code_2",
    [
        ("test1@test1.com", "Pa$$w0rd!", 200, 401),
        ("test1@test1.com", "Pa$$w0rd!", 423, 401),
        ("test1@test1", "Pa$$w0rd!", 422, 401),
        ("test1", "Pa$$w0rd!", 422, 401),
    ],
)
async def test_full_auth_flow(
    ac,
    email: str,
    password: str,
    status_code_1: int,
    status_code_2: int,
):
    # /register
    response_register = await ac.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert response_register.status_code == status_code_1
    if response_register.status_code > 250:
        return

    # /login
    response_login = await ac.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert response_login.status_code == status_code_1
    assert "access_token" in response_login.json()

    # /me
    response_me = await ac.get("/auth/me")
    assert response_me.status_code == status_code_1
    user = response_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == status_code_1
    assert "access_token" not in ac.cookies

    response_me_2 = await ac.get("/auth/me")
    assert response_me_2.status_code == status_code_2
