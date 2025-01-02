from sqlalchemy.orm import Session 
from . import models, schemas
from passlib.context import CryptContext

# Configuracion para el hashing de la contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear un nuevo estudiante
def create_student(db: Session, student: schemas.StudentCreate):
    hashed_password = hash_password(student.password)
    db_student = models.Student(
        names=student.names, 
        last_names=student.last_names, 
        email=student.email, 
        university=student.university, 
        career_university=student.career_university, 
        dateBirth=student.dateBirth, 
        age=student.age, 
        id_card=student.id_card, 
        phone_number=student.phone_number, 
        password=hashed_password)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Función para obtener un estudiante por su ID
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# Función para obtener todos los estudiantes
def get_student(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

# Función para actualizar un estudiante
def update_student(db: Session, student_id: int, student: schemas.StudentCreate):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        return None
    db_student.names = student.names
    db_student.last_names = student.last_names
    db_student.email = student.email
    db_student.university = student.university
    db_student.career_university = student.career_university
    db_student.dateBirth = student.dateBirth
    db_student.age = student.age
    db_student.id_card = student.id_card
    db_student.phone_number = student.phone_number
    db.commit()
    db.refresh(db_student)
    return db_student

# Función para eliminar un estudiante
def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        return None
    db.delete(db_student)
    db.commit()
    return db_student

