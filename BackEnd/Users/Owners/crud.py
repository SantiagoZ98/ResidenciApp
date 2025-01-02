from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def create_owner(db: Session, owner: schemas.OwnerCreate):
    hashed_password = hash_password(owner.password)
    db_owner = models.Owner(
        name=owner.name, 
        last_name=owner.last_name, 
        email=owner.email, 
        id_card=owner.id_card, 
        phone=owner.phone, 
        birth_date=owner.birth_date, 
        password=hashed_password)
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

def get_owner(db: Session, owner_id: int):
    return db.query(models.Owner).filter(models.Owner.id == owner_id).first()

def get_owners(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Owner).offset(skip).limit(limit).all()

def update_owner(db: Session, owner_id: int, owner: schemas.OwnerUpdate):
    db_owner = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
    if db_owner is None:
        return None
    db_owner.name = owner.name
    db_owner.last_name = owner.last_name
    db_owner.email = owner.email
    db_owner.id_card = owner.id_card
    db_owner.phone = owner.phone
    db_owner.birth_date = owner.birth_date
    db.commit()
    db.refresh(db_owner)
    return db_owner

def delete_owner(db: Session, owner_id: int):
    db_owner = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
    if db_owner is None:
        return None
    db.delete(db_owner)
    db.commit()
    return db_owner