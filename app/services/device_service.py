from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.device import DeviceModel
from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceCreate


class DeviceService:
    def __init__(self, db: Session):
        self.repo = DeviceRepository(db)

    @staticmethod
    def _normalize_create_payload(payload: DeviceCreate) -> dict:
        data = payload.model_dump()
        device_type = data["type"]

        if device_type == "Light" and data.get("brightness") is None:
            data["brightness"] = 100
        if device_type == "Thermostat" and data.get("temperature") is None:
            data["temperature"] = 22
        if device_type == "Camera" and not data.get("resolution"):
            data["resolution"] = "1080p"

        return data

    def list_devices(self) -> list[DeviceModel]:
        return self.repo.list_devices()

    def get_device(self, device_id: str) -> DeviceModel:
        device = self.repo.get_device(device_id)
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        return device

    def create_device(self, payload: DeviceCreate) -> DeviceModel:
        if self.repo.get_device(payload.id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Device id already exists")

        data = self._normalize_create_payload(payload)
        device = DeviceModel(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            status="off",
            energy_usage=0.0,
            brightness=data.get("brightness"),
            temperature=data.get("temperature"),
            resolution=data.get("resolution"),
        )
        return self.repo.create_device(device)

    def delete_device(self, device_id: str) -> None:
        device = self.get_device(device_id)
        self.repo.delete_device(device)

    def execute_command(self, device_id: str, command: str) -> DeviceModel:
        if command not in {"on", "off"}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid command")

        device = self.get_device(device_id)
        device.status = command
        return self.repo.save(device)

    def total_energy_usage(self) -> float:
        return self.repo.total_energy_usage()
