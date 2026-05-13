from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.device import DeviceCreate
from app.schemas.serializers import device_to_dict
from app.services.device_service import DeviceService


router = APIRouter(tags=["legacy"])


@router.get("/devices")
def legacy_list_devices(db: Session = Depends(get_db)):
    service = DeviceService(db)
    return [device_to_dict(d) for d in service.list_devices()]


@router.get("/devices/{device_id}")
def legacy_get_device(device_id: str, db: Session = Depends(get_db)):
    service = DeviceService(db)
    return device_to_dict(service.get_device(device_id))


@router.post("/devices", status_code=201)
def legacy_create_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    service = DeviceService(db)
    return device_to_dict(service.create_device(payload))


@router.post("/add_device", status_code=201)
def legacy_create_device_alt(payload: DeviceCreate, db: Session = Depends(get_db)):
    service = DeviceService(db)
    return device_to_dict(service.create_device(payload))


@router.delete("/devices/{device_id}")
def legacy_delete_device(device_id: str, db: Session = Depends(get_db)):
    service = DeviceService(db)
    service.delete_device(device_id)
    return {"message": "Device removed successfully"}


@router.put("/devices/{device_id}/{command}")
def legacy_execute_command_put(device_id: str, command: str, db: Session = Depends(get_db)):
    service = DeviceService(db)
    return device_to_dict(service.execute_command(device_id, command))


@router.get("/devices/{device_id}/{command}")
def legacy_execute_command_get(device_id: str, command: str, db: Session = Depends(get_db)):
    service = DeviceService(db)
    return device_to_dict(service.execute_command(device_id, command))


@router.get("/energy_usage")
def legacy_energy_usage(db: Session = Depends(get_db)):
    service = DeviceService(db)
    return {"total_energy_usage": service.total_energy_usage()}
