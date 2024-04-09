from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from .base import Base

user_item_association = Table(
    "user_item_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("item_id", Integer, ForeignKey("items.id")),
    Column("quantity", Integer, default=0)
)

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
    last_slutted: Mapped[int] = mapped_column(Integer(), default=0)
    last_crimed: Mapped[int] = mapped_column(Integer(), default=0)
    last_robbed: Mapped[int] = mapped_column(Integer(), default=0)

    items = relationship("Item", secondary=user_item_association, backref="users")
    created_items = relationship("Item", backref="creator")
    
    passive: Mapped[int] = mapped_column(Integer(), default=0)