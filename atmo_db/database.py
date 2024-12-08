from sqlmodel import Session, create_engine
import os

#Database setup
DB_URL = "sqlite:////app/atmo_db/atmo.db"
engine = create_engine(DB_URL, connect_args=
                      {'check_same_thread': False})

#dependency
def get_session():
  with Session(engine) as session:
    yield session