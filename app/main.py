from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from . import controllers, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Vessel
@app.get("/vessels/", response_model=list[schemas.Vessel])
def get_vessels(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return controllers.get_vessels(db, skip, limit)


@app.get("/vessels/{vessel_id}", response_model=schemas.Vessel)
def get_vessel_by_id(vessel_id: int, db: Session = Depends(get_db)):
    db_vessel = controllers.get_vessel_by_id(db, vessel_id)
    if db_vessel is None:
        raise HTTPException(status_code=404, detail="Vessel not found")
    return db_vessel


@app.get("/vessels/code/{vessel_code}", response_model=schemas.Vessel)
def get_vessel_by_code(vessel_code: str, db: Session = Depends(get_db)):
    db_vessel = controllers.get_vessel_by_code(db, vessel_code)
    if db_vessel is None:
        raise HTTPException(status_code=404, detail="Vessel not found")
    return db_vessel


@app.post("/vessels/", response_model=schemas.Vessel)
def create_vessel(vessel: schemas.VesselCreate, db: Session = Depends(get_db)):
    db_vessel = controllers.get_vessel_by_code(db, vessel.code)
    if db_vessel:
        raise HTTPException(status_code=400, detail="Code already registered")
    return controllers.create_vessel(db, vessel)


@app.get(
    "/vessels/{vessel_id}/average_cost", response_class=JSONResponse
)
def get_vessels_average_cost(vessel_id: int, db: Session = Depends(get_db)):
    vessel = controllers.get_vessel_by_id(db, vessel_id)
    if vessel:
        equipments = vessel.equipments
        orders_count = 0
        orders_total = 0
        for equipment in equipments:
            orders_count += len(equipment.orders)
            for order in equipment.orders: 
                orders_total += order.cost
        average =  orders_total / orders_count
        return {"vessel": vessel, "average_cost": round(average, 2)}
    raise HTTPException(status_code=404, detail="Vessel not found")


# Equipments
@app.get(
    "/vessels/{vessel_id}/equipments",
    response_model=list[schemas.Equipment]
)
def get_vessels_equipments(vessel_id: int, db: Session = Depends(get_db)):
    vessel = controllers.get_vessel_by_id(db, vessel_id)
    return vessel.equipments


@app.get(
    "/vessels/{vessel_id}/equipments/active",
    response_model=list[schemas.Equipment]
)
def get_vessels_active_equipments(
    vessel_id: int, db: Session = Depends(get_db)
):
    vessel = controllers.get_vessel_by_id(db, vessel_id)
    active = [x for x in vessel.equipments if x.status == 'active']
    return active

@app.post(
    "/vessels/{vessel_id}/equipments/", response_model=schemas.Equipment
)
def create_equipment_for_vessel(
    vessel_id: int, equipment: schemas.EquipmentCreate,
    db: Session = Depends(get_db)
):
    db_equipment = controllers.get_equipment_by_code(db, equipment.code)
    if db_equipment:
        raise HTTPException(
            status_code=400, detail="Equipment already registered")
        
    return controllers.create_vessel_equipment(
        db, equipment, vessel_id
    )


@app.get("/equipments/", response_model=list[schemas.Equipment])
def get_all_equipments(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return controllers.get_equipments(db, skip, limit)


@app.get("/equipments/code/{equipment_code}", response_model=schemas.Equipment)
def get_all_equipments(equipment_code: str, db: Session = Depends(get_db)):
    return controllers.get_equipment_by_code(db, equipment_code)


@app.post("/equipments/set_inactive", response_class=JSONResponse)
def set_equipments_as_inactive(
    equipment_codes: list[str], db: Session = Depends(get_db)
):
    return controllers.set_equipments_inactive(
        db=db, codes=equipment_codes
    )


# Orders
@app.get("/orders/", response_model=list[schemas.Order])
def get_orders(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return controllers.get_orders(db, skip, limit)


@app.get(
    "/equipments/{equipment_id}/orders", response_model=list[schemas.Order]
)
def get_orders_by_equipment_id(
    equipment_id: int, db: Session = Depends(get_db)
):
    return controllers.get_orders_by_equipment_id(db, equipment_id)


@app.get(
    "/equipments/code/{equipment_code}/orders/total",
    response_class=JSONResponse
)
def get_equipment_orders_total(
    equipment_code: str, db: Session = Depends(get_db)
):
    equipment = controllers.get_equipment_by_code(db, equipment_code)
    if equipment:
        total = 0
        for order in equipment.orders:
            total += order.cost
        return {"total": total}
    raise HTTPException(
        status_code=404, detail="Equipment not exists")


@app.get(
    "/equipments/name/{equipment_name}/orders/total",
    response_class=JSONResponse
)
def get_equipment_total_cost(
    equipment_name: str, db: Session = Depends(get_db)
):
    equipment = controllers.get_equipment_by_name(db, equipment_name)
    if equipment:
        total = 0
        for order in equipment.orders:
            total += order.cost
        return {"total": total}
    raise HTTPException(status_code=404, detail="Equipment not found")


@app.post("/equipments/{equipment_id}/orders", response_model=schemas.Order)
def create_equipment_order(
    equipment_id: int,
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):
    equipment = controllers.get_equipment_by_id(db, equipment_id)
    if equipment:
        return controllers.create_equipment_order(
            db, order, equipment.id
        )
    raise HTTPException(
    status_code=404, detail="Equipment not exists")


@app.post("/orders", response_model=schemas.Order)
def create_equipment_order(
    order: schemas.OrderCreateWithCode,
    db: Session = Depends(get_db)
):
    equipment = controllers.get_equipment_by_code(db, order.code)
    if equipment:
        return controllers.create_order_with_code(db, order, equipment.id)
    raise HTTPException(
    status_code=404, detail="Equipment not exists")
