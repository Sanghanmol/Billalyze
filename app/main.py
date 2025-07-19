from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.ingest import process_file
from app.db.database import engine, Base, SessionLocal
from app.db.models import Receipt
import shutil
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in [
        "image/jpeg",
        "image/png",
        "application/pdf",
        "text/plain",
    ]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        parsed_data = process_file(file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    db = SessionLocal()
    receipt = Receipt(**parsed_data)
    db.add(receipt)
    db.commit()
    db.refresh(receipt)
    db.close()

    return {"message": "File processed", "data": parsed_data}
