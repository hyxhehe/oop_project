from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.core.config import get_settings


@dataclass
class MigrationReport:
    total: int = 0
    migrated: int = 0
    failed: int = 0
    skipped: int = 0
    errors: list[dict[str, Any]] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "migrated": self.migrated,
            "failed": self.failed,
            "skipped": self.skipped,
            "errors": self.errors or [],
        }


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    device_type = row.get("type") or "Light"
    if device_type not in {"Light", "Thermostat", "Camera"}:
        device_type = "Light"

    return {
        "id": str(row.get("id", "")).strip(),
        "name": str(row.get("name", "")).strip() or "Unnamed Device",
        "status": "on" if str(row.get("status", "off")).lower() == "on" else "off",
        "energy_usage": float(row.get("energy_usage") or 0.0),
        "type": device_type,
        "brightness": float(row["brightness"]) if row.get("brightness") is not None else None,
        "temperature": float(row["temperature"]) if row.get("temperature") is not None else None,
        "resolution": str(row["resolution"]) if row.get("resolution") is not None else None,
    }


def migrate_legacy_devices() -> MigrationReport:
    settings = get_settings()
    engine = create_engine(settings.sqlalchemy_database_uri, future=True)
    report = MigrationReport(errors=[])

    with Session(engine) as session:
        rows = session.execute(
            text(
                "SELECT id, name, status, energy_usage, type, brightness, temperature, resolution FROM devices"
            )
        ).mappings().all()

        report.total = len(rows)
        for raw in rows:
            try:
                row = normalize_row(dict(raw))
                if not row["id"]:
                    report.skipped += 1
                    continue

                session.execute(
                    text(
                        """
                        INSERT INTO devices (id, name, status, energy_usage, type, brightness, temperature, resolution)
                        VALUES (:id, :name, :status, :energy_usage, :type, :brightness, :temperature, :resolution)
                        ON DUPLICATE KEY UPDATE
                            name = VALUES(name),
                            status = VALUES(status),
                            energy_usage = VALUES(energy_usage),
                            type = VALUES(type),
                            brightness = VALUES(brightness),
                            temperature = VALUES(temperature),
                            resolution = VALUES(resolution)
                        """
                    ),
                    row,
                )
                report.migrated += 1
            except Exception as exc:
                report.failed += 1
                report.errors.append({"id": raw.get("id"), "error": str(exc)})
        session.commit()

    return report


if __name__ == "__main__":
    migration_report = migrate_legacy_devices()
    print(json.dumps(migration_report.to_dict(), ensure_ascii=False, indent=2))
