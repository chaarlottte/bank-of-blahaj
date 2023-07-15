from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_username: Mapped[str] = mapped_column(String(30))
    cash: Mapped[int] = mapped_column(Integer(), default=0)
    bank: Mapped[int] = mapped_column(Integer(), default=0)
    last_collected_income: Mapped[int] = mapped_column(Integer(), default=0)