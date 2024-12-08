from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from atmo_db.database import engine
from sqlmodel import SQLModel



app = FastAPI()
@app.on_event("startup")
async def startup_event():
    print(engine)
    SQLModel.metadata.create_all(engine)


templates = Jinja2Templates(directory="templates")

@app.get("/")
def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/audio-files")
def list_files(request: Request):
    return templates.TemplateResponse("audio-files.html", {"request": request})