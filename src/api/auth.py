from fastapi import APIRouter, Response
from passlib.context import CryptContext

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import EmailNotRegisteredHTTPException, EmailNotRegisteredException, IncorrectPasswordException, \
    IncorrectPasswordHTTPException, UserAlreadyExistException, UserAlreadyExistHTTPException
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistException:
        raise UserAlreadyExistHTTPException

    return {"status": "OK"}


@router.post("/login", summary="Авторизация пользователя")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Получение информации о пользователе")
async def get_me(db: DBDep, user_id: UserIdDep):
    return await AuthService(db).get_me(user_id)


@router.post("/logout", summary="Разавторизация пользователя")
async def logout_me(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
