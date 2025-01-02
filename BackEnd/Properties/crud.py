from sqlalchemy.orm import Session
from models import Property
from schemas import PropertyCreate, PropertyUpdate

def get_properties(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Property).offset(skip).limit(limit).all()

def get_property(db: Session, property_id: int):
    return db.query(Property).filter(Property.id == property_id).first()

def create_property(db: Session, property: PropertyCreate, owner_id: int):
    db_property = Property(**property.dict(), owner_id=owner_id)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def update_property(db: Session, property_id: int, property: PropertyUpdate):
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property:
        for key, value in property.dict(exclude_unset=True).items():
            setattr(db_property, key, value)
        db.commit()
        db.refresh(db_property)
    return db_property

def delete_property(db: Session, property_id: int):
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property:
        db.delete(db_property)
        db.commit()
    return db_property
