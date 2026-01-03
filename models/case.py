from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from core.database import Base


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    patient_key = Column(String(64), index=True)
    year = Column(Integer)
    pathway = Column(String(16))  # CS / PRIMI / MULTI
    is_cs = Column(Boolean, default=False)
    is_primipara = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
