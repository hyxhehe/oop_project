from app.models.device import DeviceModel


def device_to_dict(device: DeviceModel) -> dict:
    return {
        "id": device.id,
        "name": device.name,
        "status": device.status,
        "type": device.type,
        "energy_usage": float(device.energy_usage),
        "brightness": device.brightness,
        "temperature": device.temperature,
        "resolution": device.resolution,
    }
