from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    id_card = Column(String(20), unique=True, nullable=False) 
    phone = Column(String, index=True)
    birth_date = Column(Date)
    password = Column(String(255), nullable=False)

    
