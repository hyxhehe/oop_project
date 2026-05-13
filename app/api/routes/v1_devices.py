from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.device import DeviceCreate, EnergyUsageResponse, APIResponse
from app.schemas.serializers import device_to_dict
from app.services.device_service import DeviceService


router = APIRouter(prefix="/api/v1", tags=["devices-v1"])


@router.get("/devices")
def list_devices(db: Session = Depends(get_db)):
    service = DeviceService(db)
    return [device_to_dict(d) for d in service.list_devices()]


@router.get("/devices/{device_id}")
def get_device(device_id: str, db: Session = Depends(get_db)):
    service = DeviceService(db)
    return device_to_dict(service.get_device(device_id))


@router.post("/devices", status_code=201)
def create_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    service = DeviceService(db)
    return device_to_dict(service.create_device(payload))


@router.delete("/devices/{device_id}", response_model=APIResponse)
def delete_device(device_id: str, db: Session = Depends(get_db)):
    service = DeviceService(db)
    service.delete_device(device_id)
    return APIResponse(message="Device removed successfully")


@router.put("/devices/{device_id}/commands/{command}")
def execute_command(device_id: str, command: str, db: Session = Depends(get_db)):
    service = DeviceService(db)
    return device_to_dict(service.execute_command(device_id, command))


@router.get("/energy-usage", response_model=EnergyUsageResponse)
def total_energy_usage(db: Session = Depends(get_db)):
    service = DeviceService(db)
    return EnergyUsageResponse(total_energy_usage=service.total_energy_usage())
