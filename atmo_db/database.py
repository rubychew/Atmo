from sqlmodel import Session, SQLModel, create_engine

#Database setup
DB_NAME = 'atmo.db'
DB_URL = f'sqlite:///./atmo_db/{DB_NAME}'
engine = create_engine(DB_URL, connect_args=
                      {'check_same_thread': False})

SQLModel.metadata.create_all(engine) #move to main?

#dependency
def get_session():
  with Session(engine) as session:
    yield session