import datetime
from typing import List, Optional

from pydantic import BaseModel

# Campos que o cliente envia ao criar um evento
class Event(BaseModel):
    id: Optional[int] = None 
    title: str
    image: str
    description: str
    tags: List[str] 
    location: str
    
    
    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }



   
        