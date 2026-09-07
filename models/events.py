from typing import Optional, List
from sqlmodel import SQLModel, Field
from sqlalchemy import JSON

class EventBase(SQLModel):
    title: str = Field(index=True)
    description: str
    location: str
    date: str
    organizer: str
    image: Optional[str] = None
    capacity: Optional[int] = None

class Event(EventBase, table=True):
    __tablename__ = "events"

    id: Optional[int] = Field(default=None, primary_key=True)
    tags: List[str] = Field(default=[], sa_type=JSON)
    organizer_id: Optional[int] = Field(default=None, foreign_key="users.id")

class EventCreate(EventBase):
    tags: List[str] = Field(default_factory=list)

class EventUpdateSchema(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date: Optional[str] = None
    organizer: Optional[str] = None
    image: Optional[str] = None
    capacity: Optional[int] = None
    tags: Optional[List[str]] = None

class EventPublicSchema(EventBase):
    id: int
    tags: List[str] = Field(default_factory=list)
    organizer_id: Optional[int] = None