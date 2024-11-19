from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRequestAdd(BaseModel):
    email: EmailStr = Field(description="Электронная почта пользователя")
    password: str = Field(description="Пароль пользователя (сырой)")


class UserAdd(BaseModel):
    email: EmailStr = Field(description="Электронная почта пользователя")
    hashed_password: str = Field(description="Пароль пользователя (хэшированный)")


class User(BaseModel):
    id: int = Field(description="ID пользователя")
    email: EmailStr = Field(description="Электронная почта пользователя")
    nickname: str | None = Field(description="Ник пользователя")
    first_name: str | None = Field(description="Имя пользователя")
    last_name: str | None = Field(description="Фамилия пользователя")

    model_config = ConfigDict(from_attributes=True)
