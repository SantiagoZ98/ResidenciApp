from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from mongodb import db
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from gridfs import GridFS
import shutil
import os
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
UPLOAD_FOLDER = "uploads/"

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["ResidenciasDB"]
fs = GridFS(db)

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/properties/", response_model=schemas.PropertyOut)
def create_property(property: schemas.PropertyCreate, db: Session = Depends(get_db), owner_id: int = 1):
    return crud.create_property(db=db, property=property, owner_id=owner_id)

@app.get("/properties/", response_model=list[schemas.PropertyOut])
def read_properties(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_properties(db, skip=skip, limit=limit)

@app.get("/properties/{property_id}", response_model=schemas.PropertyOut)
def read_property(property_id: int, db: Session = Depends(get_db)):
    property = crud.get_property(db, property_id=property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@app.put("/properties/{property_id}", response_model=schemas.PropertyOut)
def update_property(property_id: int, property: schemas.PropertyUpdate, db: Session = Depends(get_db)):
    updated_property = crud.update_property(db, property_id=property_id, property=property)
    if not updated_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return updated_property

@app.delete("/properties/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    deleted_property = crud.delete_property(db, property_id=property_id)
    if not deleted_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"detail": "Property deleted"}

@app.post("/files/upload/")
async def upload_file(file: UploadFile, property_id: int):
    # Guardar el archivo temporalmente en el servidor
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Obtener metadatos del archivo
    file_metadata = {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": os.path.getsize(file_path),
        "property_id": property_id
    }

    # Guardar los metadatos en MongoDB
    result = await db["files"].insert_one(file_metadata)

    # Opcional: Eliminar el archivo temporal o moverlo a un almacenamiento permanente
    os.remove(file_path)

    return {"file_id": str(result.inserted_id), "message": "File uploaded successfully"}

@app.get("/files/{file_id}")
async def get_file(file_id: str):
    # Buscar el archivo en MongoDB
    file_metadata = await db["files"].find_one({"_id": ObjectId(file_id)})
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    return {
        "filename": file_metadata["filename"],
        "content_type": file_metadata["content_type"],
        "size": file_metadata["size"],
        "property_id": file_metadata["property_id"]
    }

@app.post("/files/upload_gridfs/")
async def upload_file_to_gridfs(file: UploadFile, property_id: int):
    # Subir archivo a GridFS
    file_id = fs.put(file.file, filename=file.filename, content_type=file.content_type, property_id=property_id)
    return {"file_id": str(file_id), "message": "File uploaded to GridFS successfully"}

@app.get("/files/gridfs/{file_id}")
async def get_file_from_gridfs(file_id: str):
    # Descargar archivo desde GridFS
    grid_out = fs.get(ObjectId(file_id))
    return {
        "filename": grid_out.filename,
        "content_type": grid_out.content_type,
        "size": grid_out.length,
        "property_id": grid_out.property_id
    }

@app.get("/properties/{property_id}/files/")
async def get_property_files(property_id: int):
    files = await db["files"].find({"property_id": property_id}).to_list(length=100)
    return files