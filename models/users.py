from pydantic import BaseModel, EmailStr
 pwd_context = Cryp

class User(BaseModel):
    id: int
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "email": "fastapi@packt.com",
                "password": "strong!!!",
            }
        }


class UserSignIn(BaseModel):
    id: str
    email: str
    password: str

    schema_extra = {
        "example": {
            "id":"1",
            "email": "fastapi@packt.com",
            "password": "strong!!!"
        }
    }
