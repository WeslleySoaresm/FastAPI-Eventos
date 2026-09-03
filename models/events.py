from typing import List, Optional
from pydantic import BaseModel

class Event(BaseModel):
    id: Optional[int] = None 
    title: str
    date: str
    organizer: str
    organizer_id: Optional[int] = None
    image: Optional[str] = None
    description: str
    tags: List[str] 
    location: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "date": "2026-09-20",
                "organizer": "Organizador",
                "image": "https://linktomyimage.com/image.png",
                "description": "Discussing FastAPI contents.",
                "tags": ["python", "fastapi"],
                "location": "Google Meet"
            }
        }

class EventPublicSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    location: Optional[str] = None

    class Config:
        from_attributes = True

class EventUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None