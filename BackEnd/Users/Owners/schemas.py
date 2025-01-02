from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class OwnerBase(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    id_card: str
    phone: Optional[str] = None
    birth_date: Optional[date] = None

class OwnerCreate(OwnerBase):
    password: str

class OwnerUpdate(OwnerBase):
    pass

class OwnerResponse(OwnerBase):
    id: int

    class Config:
        orm_mode = True