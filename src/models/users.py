from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import Base


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    nickname: Mapped[str | None] = mapped_column(String(100))
    first_name: Mapped[str | None] = mapped_column(String(150))
    last_name: Mapped[str | None] = mapped_column(String(150))
