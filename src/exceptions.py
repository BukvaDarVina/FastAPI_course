from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class ObjectAlreadyExistException(NabronirovalException):
    detail = "Похожий объект уже существует"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class EmailAlreadyExistException(NabronirovalException):
    detail = "Пользователь с такой почтой уже имеется"


class IncorrectTokenException(NabronirovalException):
    detail = "Неверный токен"


class EmailNotRegisteredException(NabronirovalException):
    detail = "Пользователь с такой почтой не зарегистрирован"


class IncorrectPasswordException(NabronirovalException):
    detail = "Пароль неверный"


class UserAlreadyExistException(NabronirovalException):
    detail = "Такой пользователь уже имеется"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата выезда не может быть раньше даты заезда")


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"


class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class IncorrectTokenHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Неверный токен"


class EmailAlreadyExistHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже имеется"


class UserAlreadyExistHTTPException(NabronirovalHTTPException):
    status_code = 423
    detail = "Такой пользователь уже существует"


class EmailNotRegisteredHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Пользователь с такой почтой не зарегистрирован"


class IncorrectPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Пароль неверный"


class NoAccessTokenHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Пароль неверный"
