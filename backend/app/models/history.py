from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base


class PartHistory(Base):
    __tablename__ = "part_history"

    id = Column(Integer, primary_key=True)
    part_id = Column(Integer)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)