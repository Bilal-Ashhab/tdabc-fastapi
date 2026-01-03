from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey("cases.id"), index=True)
    event_type = Column(String(32))
    actor_role = Column(String(32))
    ts = Column(DateTime(timezone=True), server_default=func.now())
