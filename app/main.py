from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes.v1_devices import router as v1_router
from app.api.routes.legacy import router as legacy_router
from app.api.routes.ui import router as ui_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import Base, engine


settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title="Smart Home API", version="2.0.0")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"error": "Validation error", "details": exc.errors()})


app.include_router(ui_router)
app.include_router(v1_router)
if settings.enable_legacy_routes:
    app.include_router(legacy_router)
