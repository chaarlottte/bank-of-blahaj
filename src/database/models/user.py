from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from .base import Base
from .user_store import UserStore  # Import UserStore model

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_username: Mapped[str] = mapped_column(String(30))
    cash: Mapped[int] = mapped_column(Integer(), default=0)
    bank: Mapped[int] = mapped_column(Integer(), default=0)

    job_id: Mapped[int] = mapped_column(Integer(), default=0)
    job_xp: Mapped[int] = mapped_column(Integer(), default=0)

    last_collected_income: Mapped[int] = mapped_column(Integer(), default=0)
    last_worked: Mapped[int] = mapped_column(Integer(), default=0)
    store_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_stores.id"), nullable=True)

    store: Mapped[UserStore] = relationship("UserStore", backref="user_store", uselist=False, foreign_keys=[store_id])
