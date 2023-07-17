from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Column, Table
from .base import Base

store_item_association = Table(
    "store_item_association",
    Base.metadata,
    Column("store_id", Integer, ForeignKey("user_stores.id")),
    Column("item_id", Integer, ForeignKey("items.id")),
    Column("quantity", Integer, default=0)
)

class UserStore(Base):
    __tablename__ = "user_stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))
    user_id = mapped_column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("User", backref="user_store", foreign_keys=[user_id])
    items = relationship("Item", backref="store_items")