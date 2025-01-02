from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # Título de la propiedad
    description = Column(String(500), nullable=True)  # Descripción
    price = Column(Float, nullable=False)  # Precio
    address = Column(String(255), nullable=False)  # Dirección
    is_available = Column(Boolean, default=True)  # Disponibilidad
    owner_id = Column(Integer, ForeignKey("users.id"))  # Propietario (relación)
