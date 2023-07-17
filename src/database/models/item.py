from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from .base import Base

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))
    price: Mapped[int] = mapped_column(Integer)
    user_store_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_stores.id"))

    user_store = relationship("UserStore", backref="store_items")