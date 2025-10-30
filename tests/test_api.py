import uuid
import requests

BASE = "http://localhost:8000"

def test_create_device_and_battery_and_attach_detach():
    # создание устройства
    r = requests.post(url=f"{BASE}/devices/", json={
        "name": f"Device-test-{uuid.uuid4().hex[:6]}",
        "firmware_version": "1.0.0",
        "status": "off"
    })
    assert r.status_code == 201
    device = r.json()
    device_id = device["id"]

    # создание АКБ
    r = requests.post(url=f"{BASE}/batteries/", json={
        "name": f"Battery-test-{uuid.uuid4().hex[:6]}",
        "nominal_voltage": 12.0,
        "remaining_capacity": 50.0,
        "lifetime": 12
    })
    assert r.status_code == 201
    battery = r.json()
    battery_id = battery["id"]

    # прикрепить АКБ
    r = requests.post(url=f"{BASE}/batteries/{battery_id}/attach/to/{device_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["device_id"] == device_id

    # открепить АКБ
    r = requests.post(url=f"{BASE}/batteries/{battery_id}/detach/from/{device_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["device_id"] is None

def test_list_device_batteries_limit():
    # создать устройство
    r = requests.post(url=f"{BASE}/devices/", json={
        "name": f"Device-limit-{uuid.uuid4().hex[:6]}",
        "firmware_version": "1.0.0",
        "status": "off"
    })
    assert r.status_code == 201
    device_id = r.json()["id"]

    # создать и прикрепить 5 АКБ
    created = []
    for i in range(5):
        rb = requests.post(url=f"{BASE}/batteries/", json={
            "name": f"Battery-limit-{uuid.uuid4().hex[:6]}",
            "nominal_voltage": 12.0,
            "remaining_capacity": 80.0,
            "lifetime": 24
        })
        assert rb.status_code == 201
        bid = rb.json()["id"]
        ra = requests.post(url=f"{BASE}/batteries/{bid}/attach/to/{device_id}")
        assert ra.status_code == 200
        created.append(bid)

    # создать 6-ю АКБ и пробуем прикрепить -> должен быть ответ 400
    rb6 = requests.post(url=f"{BASE}/batteries/", json={
        "name": f"Battery-limit-{uuid.uuid4().hex[:6]}",
        "nominal_voltage": 12.0,
        "remaining_capacity": 80.0,
        "lifetime": 24
    })
    assert rb6.status_code == 201
    bid6 = rb6.json()["id"]
    ra6 = requests.post(url=f"{BASE}/batteries/{bid6}/attach/to/{device_id}")
    assert ra6.status_code == 400
