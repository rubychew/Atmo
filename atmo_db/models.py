from sqlmodel import SQLModel, Field, Relationship
from datatime import datetime
from pydantic import AnyUrl

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    #need username, email address, password
    username: str
    email: str
    role: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
    last_login: datetime | None = None
    is_logged_in: bool = Field(default=False)
    audio_files: list['Audio_File'] = Relationship(back_populates='user')
    password: str

class Audio_File(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    description: str | None = None
    file_type: str
    url: AnyUrl
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
    user_id: int | None = Field(default=None, foreign_key='user.id')
    user: User | None = Relationship(back_populates='audio_files')