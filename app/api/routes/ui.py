from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["ui"])
BASE_DIR = Path(__file__).resolve().parents[3]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/ui/devices", response_class=HTMLResponse)
def devices_page(request: Request):
    return templates.TemplateResponse("devicelist.html", {"request": request})


@router.get("/ui/add_device", response_class=HTMLResponse)
def add_device_page(request: Request):
    return templates.TemplateResponse("add_advice.html", {"request": request})


@router.get("/ui/remove_device", response_class=HTMLResponse)
def remove_device_page(request: Request):
    return templates.TemplateResponse("remove_device.html", {"request": request})


@router.get("/ui/device_control", response_class=HTMLResponse)
def device_control_page(request: Request):
    return templates.TemplateResponse("device_status.html", {"request": request, "device_id": "", "device_name": "", "status": "off"})


# legacy page aliases
@router.get("/add_device", response_class=HTMLResponse)
def add_device_legacy(request: Request):
    return templates.TemplateResponse("add_advice.html", {"request": request})


@router.get("/remove_device", response_class=HTMLResponse)
def remove_device_legacy(request: Request):
    return templates.TemplateResponse("remove_device.html", {"request": request})


@router.get("/device_control", response_class=HTMLResponse)
def device_control_legacy(request: Request):
    return templates.TemplateResponse("device_status.html", {"request": request, "device_id": "", "device_name": "", "status": "off"})
