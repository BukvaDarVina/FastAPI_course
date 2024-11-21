from fastapi import APIRouter, Response, HTTPException
from passlib.context import CryptContext

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", summary="Регистрация пользователя")
async def register_user(db: DBDep, data: UserRequestAdd,):
    hashed_password = AuthService().hash_password(data.password)
    try:
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await db.users.add(new_user_data)
        await db.session.commit()
        return {"status": "OK"}
    except Exception:
        raise HTTPException(status_code=423, detail="Пользователь с таким email уже зарегистрирован. "
                                                    "Используйте другой email.")


@router.post("/login", summary="Авторизация пользователя")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Получение информации о пользователе")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout", summary="Разавторизация пользователя")
async def logout_me(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
