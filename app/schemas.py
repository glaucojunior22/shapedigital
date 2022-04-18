from typing import Optional
from pydantic import BaseModel


class OrderBase(BaseModel):
    type: str
    cost: float


class OrderCreate(OrderBase):
    pass


class OrderCreateWithCode(OrderBase):
    code: str


class Order(OrderBase):
    id: int
    equipment_id: int

    class Config:
        orm_mode = True


class EquipmentBase(BaseModel):
    name: str
    code: str
    location: str
    status: Optional[str] = None


class EquipmentCreate(EquipmentBase):
    pass


class Equipment(EquipmentBase):
    id: int
    vessel_id: int
    orders: list[Order] = []

    class Config:
        orm_mode = True


class VesselBase(BaseModel):
    code: str


class VesselCreate(VesselBase):
    pass


class Vessel(VesselBase):
    id: int
    equipments: list[Equipment] = []

    class Config:
        orm_mode = True
