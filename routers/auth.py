from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_sign_in(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/auth/", status_code=200)
async def auth():
    return { "auth" : "ok"}

