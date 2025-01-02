from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Strudent(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True) # Primary key ID 
    names = Column(String(100), nullable=False) # Nombre del estudiante
    last_names = Column(String(100), nullable=False) # Apellidos del estudiante
    email = Column(String(100), unique=True, nullable=False) # Correo electronico del estudiante
    university = Column(String(100), nullable=False) # Universidad del estudiante
    career_university = Column(String(100), nullable=False) # Carrera universitaria del estudiante
    dateBirth = Column(Date, nullable=False) # Fecha de nacimiento del estudiante
    age = Column(Integer(10)) # Edad del estudiante
    id_card = Column(String(20), unique = False, nullable=False) # Numero de cedula del estudiante
    phone_number = Column(String(15), nullable=False) # Numero de telefono del estudiante
    password = Column(String(255), nullable=False) # Contraseña del estudiante