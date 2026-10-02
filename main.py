from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# ---------- Task 1: Model the Shipment ----------
def compute_status(delay_days: int) -> str:
    if delay_days <= 0:
        return "on_time"
    elif delay_days <= 2:
        return "minor_delay"
    else:
        return "major_delay"


class Shipment:
    def __init__(self, shipment_id: str, carrier: str, delay_days: int):
        self.shipment_id = shipment_id
        self.carrier = carrier
        self.delay_days = delay_days

    def status(self) -> str:
        return compute_status(self.delay_days)


# ---------- Task 2: API Endpoints ----------
app = FastAPI()
shipments_db = {}


class ShipmentIn(BaseModel):
    carrier: str
    delay_days: int


@app.get("/shipments/{shipment_id}")
def get_shipment(shipment_id: str):
    if shipment_id not in shipments_db:
        raise HTTPException(status_code=404, detail="Shipment not found")
    s = shipments_db[shipment_id]
    return {"shipment_id": s.shipment_id, "carrier": s.carrier,
            "delay_days": s.delay_days, "status": s.status()}


@app.post("/shipments/{shipment_id}")
def create_shipment(shipment_id: str, shipment: ShipmentIn):
    s = Shipment(shipment_id, shipment.carrier, shipment.delay_days)
    shipments_db[shipment_id] = s
    return {"shipment_id": s.shipment_id, "carrier": s.carrier,
            "delay_days": s.delay_days, "status": s.status()}