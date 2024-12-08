from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    username: str
    email: str
    role: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    last_login: datetime | None = None
    is_logged_in: bool = Field(default=False)
    audio_files: list['Audio_File'] | None = Relationship(back_populates='user')
    password: str

class Audio_File(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    description: str | None = None
    file_type: str
    url: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    user_id: int | None = Field(default=None, foreign_key='user.id')
    user: User | None = Relationship(back_populates='audio_files')