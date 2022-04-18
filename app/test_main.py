from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

vessel_data = {"code": "VM102"}
equipment_data = {
    "name": "compressor", "code": "5310B9D7", "location": "Brazil"
}
order_data = {"code": "5310B9D7", "type": "replacement", "cost": 10000}

# Docs
def test_docs():
    res = client.get("/docs")
    assert res.status_code == 200


def test_redoc():
    res = client.get("/redoc")
    assert res.status_code == 200


# Vessel
def test_list_vessels():
    res = client.get("/vessels")
    assert res.status_code == 200
    assert res.json() == []


def test_create_vessel():
    res = client.post("/vessels/", json=vessel_data)
    assert res.status_code == 200
    assert res.json() == {
        "code": "VM102",
        "id": 1,
        "equipments": []
    }


def test_create_repeated_vessel():
    res = client.post("/vessels/", json=vessel_data)
    assert res.status_code == 400
    assert res.json() == {
        "detail": "Code already registered"
    }


# Equipment
def test_list_equipments():
    res = client.get("/equipments")
    assert res.status_code == 200
    assert res.json() == []


def test_create_vessel_equipment():
    res = client.post("/vessels/1/equipments/", json=equipment_data)
    assert res.status_code == 200
    assert res.json() == {
        "name": equipment_data["name"],
        "code": equipment_data["code"],
        "location": equipment_data["location"],
        "status": "active",
        "id": 1,
        "vessel_id": 1,
        "orders": []
    }


def test_create_repeated_equipment():
    res = client.post("/vessels/1/equipments/", json=equipment_data)
    assert res.status_code == 400
    assert res.json() == {
        "detail": "Equipment already registered"
    }


def test_get_active_equipments_by_vessel():
    res = client.get("/vessels/1/equipments/active/")
    assert res.status_code == 200
    assert res.json() == [
        {
            "name": equipment_data["name"],
            "code": equipment_data["code"],
            "location": equipment_data["location"],
            "status": "active",
            "id": 1,
            "vessel_id": 1,
            "orders": []
        }
    ]


def test_set_equipment_inactive():
    res = client.post("/equipments/set_inactive", json=["5310B9D7", "ABC123"])
    assert res.status_code == 200
    assert res.json() == {
        "success": ["5310B9D7"], "errors": ["ABC123"]
    }


# Order
def test_create_order():
    res = client.post("/orders", json=order_data)
    assert res.status_code == 200
    assert res.json() == {
        "type": order_data["type"],
        "cost": order_data["cost"],
        "id": 1,
        "equipment_id": 1
    }


def test_get_total_cost_by_equipment_code():
    res = client.get(f"/equipments/code/{equipment_data['code']}/orders/total")
    assert res.status_code == 200
    assert res.json() == {"total": order_data["cost"]}


def test_get_total_cost_by_equipment_name():
    res = client.get(f"/equipments/name/{equipment_data['name']}/orders/total")
    assert res.status_code == 200
    assert res.json() == {"total": order_data["cost"]}


def test_get_average_cost_by_vessel_id():
    res = client.get(f"/vessels/1/average_cost")
    assert res.status_code == 200
    assert res.json()["average_cost"] == order_data["cost"]
