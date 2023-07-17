from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from .base import Base

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))
    price: Mapped[int] = mapped_column(Integer)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    creator_user = relationship("User", backref="items_created")