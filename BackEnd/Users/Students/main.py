from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

# Crear la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la session de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db=db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    update_student = crud.update_student(db=db, student_id=student_id, student=student)
    if update_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return update_student

@app.delete("/students/{student_id}", response_model=schemas.StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    delete_student = crud.delete_student(db=db, student_id=student_id)
    if delete_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return delete_student