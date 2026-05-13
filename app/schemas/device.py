from typing import Literal
from pydantic import BaseModel, Field


DeviceType = Literal["Light", "Thermostat", "Camera"]
DeviceCommand = Literal["on", "off"]


class DeviceBase(BaseModel):
    id: str = Field(min_length=1, max_length=255)
    name: str = Field(min_length=1, max_length=255)
    type: DeviceType
    status: str = "off"
    energy_usage: float = 0.0
    brightness: float | None = None
    temperature: float | None = None
    resolution: str | None = None


class DeviceCreate(BaseModel):
    id: str = Field(min_length=1, max_length=255)
    name: str = Field(min_length=1, max_length=255)
    type: DeviceType
    brightness: float | None = None
    temperature: float | None = None
    resolution: str | None = None


class DeviceResponse(DeviceBase):
    pass


class EnergyUsageResponse(BaseModel):
    total_energy_usage: float


class APIResponse(BaseModel):
    message: str
