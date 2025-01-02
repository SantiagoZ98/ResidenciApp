from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

# Crear la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/owners/", response_model=schemas.OwnerResponse)
def create_owner(owner: schemas.OwnerCreate, db: Session = Depends(get_db)):
    return crud.create_owner(db=db, owner=owner)

@app.get("/owners/{owner_id}", response_model=schemas.OwnerResponse)
def read_owner(owner_id: int, db: Session = Depends(get_db)):
    db_owner = crud.get_owner(db=db, owner_id=owner_id)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return db_owner

@app.get("/owners/{owner_id}", response_model=schemas.OwnerResponse)
def update_owner(owner_id: int, owner: schemas.OwnerUpdate, db: Session = Depends(get_db)):
    update_owner = crud.update_owner(db=db, owner_id=owner_id, owner=owner)
    if update_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return update_owner

@app.delete("/owners/{owner_id}", response_model=schemas.OwnerResponse)
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    delete_owner = crud.delete_owner(db=db, owner_id=owner_id)
    if delete_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return delete_owner