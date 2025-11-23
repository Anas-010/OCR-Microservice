from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
import uuid
from datetime import datetime
from database import db
from ocr_engine import extract_text_from_pdf
from parser import parse_text
from models import OCRResponse, OCRResult, ExtractedData

app = FastAPI(title="OCR Microservice")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
def startup_db_client():
    db.connect()

@app.on_event("shutdown")
def shutdown_db_client():
    db.close()

@app.post("/upload", response_model=OCRResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Generate unique ID
    doc_id = str(uuid.uuid4())
    file_location = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")
    
    # Save file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. OCR
        raw_text = extract_text_from_pdf(file_location)
        
        # 2. Parse
        parsed_data = parse_text(raw_text)
        
        # 3. Store in MongoDB
        document = {
            "_id": doc_id,
            "filename": file.filename,
            "upload_date": datetime.utcnow(),
            "status": "processed",
            "extracted_data": parsed_data
        }
        
        # Use the 'documents' collection
        db.get_collection("documents").insert_one(document)
        
        return JSONResponse(status_code=200, content={"doc_id": doc_id, "message": "File processed and stored successfully"})

    except Exception as e:
        # Log error and return 500
        print(f"Processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/results/{doc_id}", response_model=OCRResult)
async def get_results(doc_id: str):
    doc = db.get_collection("documents").find_one({"_id": doc_id})
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {
        "filename": doc["filename"],
        "status": doc["status"],
        "extracted_data": doc["extracted_data"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
