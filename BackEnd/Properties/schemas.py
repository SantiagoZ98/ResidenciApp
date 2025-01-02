from pydantic import BaseModel
from typing import Optional

class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    address: str
    is_available: Optional[bool] = True

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    pass

class PropertyOut(PropertyBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class FileMetadata(BaseModel):
    filename: str
    content_type: str
    size: int
    property_id: Optional[int]  # Relación con una propiedad en MySQL
