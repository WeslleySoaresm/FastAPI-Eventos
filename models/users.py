from typing import Optional
from pydantic import ConfigDict, EmailStr
from sqlmodel import SQLModel, Field

# Tabela do Banco de Dados
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="participante")

# Schemas de Entrada / DTOs
class UserSignIn(SQLModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!"
            }
        }
    )