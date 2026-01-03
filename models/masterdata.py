from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from core.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    type = Column(String(32))     # staff / room / equipment
    role = Column(String(32))     # nurse / physician / team


class CapacityRate(Base):
    __tablename__ = "capacity_rates"

    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey("resources.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    cost_per_minute = Column(Float)
