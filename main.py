from fastapi import FastAPI
from atmo_db.database import engine
from sqlmodel import SQLModel
# Model imports required for the engine to create the schema
from atmo_db.models import User, Audio_File

from routers import auth, audio_files

app = FastAPI()

#create db schema on startup
@app.on_event("startup")
async def startup_event():
    SQLModel.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(audio_files.router)