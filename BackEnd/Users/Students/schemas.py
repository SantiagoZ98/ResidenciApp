from pydantic import BaseModel, EmailStr 

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True

class StudentResponse(StudentBase):
    id: int

    class Config:
        orm_mode = True