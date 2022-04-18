from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .db import Base


class Vessel(Base):
    __tablename__ = "vessel"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)

    equipments = relationship("Equipment", back_populates="vessel")


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    location = Column(String, index=True)
    status = Column(String, index=True, default='active')
    vessel_id = Column(Integer, ForeignKey("vessel.id"))

    vessel = relationship("Vessel", back_populates="equipments")
    orders = relationship("Order", back_populates="equipment")


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    cost = Column(Float(10, 2))
    equipment_id = Column(Integer, ForeignKey("equipment.id"))

    equipment = relationship("Equipment", back_populates="orders")
