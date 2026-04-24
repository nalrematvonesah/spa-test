from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.base import Base


class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    quantity = Column(Integer, default=1)

    parent_id = Column(
        Integer,
        ForeignKey("parts.id", ondelete="CASCADE"),
        nullable=True
    )

    parent = relationship(
        "Part",
        remote_side=[id],
        back_populates="children"
    )

    children = relationship(
        "Part",
        back_populates="parent",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin"
    )