from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from .models import Vessel, Equipment, Order
from . import schemas


# Vessel
def get_vessels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Vessel).offset(skip).limit(limit).all()


def get_vessel_by_id(db: Session, id: int):
    return db.query(Vessel).filter(
        Vessel.id == id
    ).first()


def get_vessel_by_code(db: Session, code: str):
    return db.query(Vessel).filter(Vessel.code == code).first()


def create_vessel(db: Session, vessel: schemas.VesselCreate):
    db_vessel = Vessel(**vessel.dict())
    db.add(db_vessel)
    db.commit()
    db.refresh(db_vessel)
    return db_vessel


def get_average_cost_by_vessel(db: Session, id: int):
    equipments = db.query(Equipment).filter_by(vessel_id=id).all()
    equipment_ids = [x.id for x in equipments]
    print(equipment_ids)
    return db.query(func.avg(Order.cost).label('average')).filter(
        Order.equipment_id.in_(equipment_ids)
    )

#Equipment
def get_equipments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Equipment).offset(skip).limit(limit).all()


def get_equipment_by_id(db: Session, id: int):
    return db.query(Equipment).filter(
        Equipment.id == id
    ).first()


def get_equipment_by_code(db: Session, code: str):
    return db.query(Equipment).filter(Equipment.code == code).first()


def get_equipment_by_name(db: Session, equipment_name: str):
    return db.query(Equipment).filter_by(name=equipment_name).first()

def get_vessel_equipments(
    db: Session, vessel_id: int, skip:int = 0, limit: int = 100
):
    print(vessel_id)
    return db.query(Equipment).filter(
        Equipment.vessel_id == vessel_id
    ).offset(skip).limit(limit).all()


def get_vessel_active_equipments(
    db: Session, vessel_id: int, skip:int = 0, limit: int = 100
):
    return db.query(Equipment).filter_by(
        vessel_id=vessel_id, status='active'
    ).offset(skip).limit(limit).all()


def create_vessel_equipment(
    db: Session, equipment: schemas.EquipmentCreate, vessel_id: int
):
    db_equipment = Equipment(**equipment.dict(), vessel_id=vessel_id)
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


def set_equipments_inactive(db: Session, codes: list[str]):
    success = []
    errors = []
    for code in codes:
        equipment = get_equipment_by_code(db, code)
        if equipment:
            equipment.status = 'inactive'
            db.commit()
            db.refresh(equipment)
            success.append(code)
        else:
            errors.append(code)
    return {"success": success, "errors": errors}


# Order
def get_orders(db: Session, skip: int, limit: int):
    return db.query(Order).offset(skip).limit(limit).all()


def create_order_with_code(
    db: Session, order: schemas.OrderCreateWithCode, equipment_id: int
):
    order_dict = order.dict()
    del(order_dict["code"])
    db_order = Order(**order_dict, equipment_id=equipment_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders_by_equipment_id(db: Session, equipment_id: int):
    db_equipment = db.query(Equipment).filter_by(id=equipment_id).first()
    return db_equipment.orders


def get_equipment_orders_total(db:Session, code: str):
    equipment = get_equipment_by_code(db, code)
    total = 0
    if equipment:
        for order in equipment.orders:
            total += order.cost
    return total


def create_equipment_order(
    db: Session, order: schemas.OrderCreate, equipment_id: int
):
    db_order = Order(**order.dict(), equipment_id=equipment_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

