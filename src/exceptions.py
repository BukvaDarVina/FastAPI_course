class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class ObjectAlreadyExistException(NabronirovalException):
    detail = "Такой объект уже есть"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class EmailAlreadyExistException(NabronirovalException):
    detail = "Пользователь с такой почтой уже имеется"
