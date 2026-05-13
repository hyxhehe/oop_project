from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.device import DeviceModel


class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_devices(self) -> list[DeviceModel]:
        stmt = select(DeviceModel)
        return list(self.db.scalars(stmt).all())

    def get_device(self, device_id: str) -> DeviceModel | None:
        return self.db.get(DeviceModel, device_id)

    def create_device(self, device: DeviceModel) -> DeviceModel:
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def delete_device(self, device: DeviceModel) -> None:
        self.db.delete(device)
        self.db.commit()

    def save(self, device: DeviceModel) -> DeviceModel:
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def total_energy_usage(self) -> float:
        stmt = select(func.coalesce(func.sum(DeviceModel.energy_usage), 0.0))
        return float(self.db.scalar(stmt) or 0.0)
