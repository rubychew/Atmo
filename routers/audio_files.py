from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/audio-files/")
def list_files(request: Request):
    return templates.TemplateResponse("audio-files.html", {"request": request})