from pydantic import BaseModel, EmailStr 

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        orm_mode = True