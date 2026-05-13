# Smart Home Project (FastAPI Refactor)

## 1) Install
```bash
pip install -r requirements.txt
```

## 2) Configure
```bash
copy .env.example .env
```
Set `DATABASE_URL` first. If not set, app will fallback to legacy `DB_*` env vars.

## 3) Run
```bash
python app.py
```
Open docs: `http://127.0.0.1:8000/docs`

## 4) Migrate schema
```bash
alembic upgrade head
```

## 5) Run legacy migration script
```bash
python -m scripts.migrate_legacy_devices
```

## 6) Run tests
```bash
pytest
```

## API
- v1: `/api/v1/devices`, `/api/v1/energy-usage`
- legacy compatible: `/devices`, `/devices/{id}`, `/devices/{id}/{command}`, `/energy_usage`, `/add_device`
