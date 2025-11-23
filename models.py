from pydantic import BaseModel
from typing import List, Optional, Any

class ExtractedData(BaseModel):
    sections: List[dict] = []
    raw_text: str

class OCRResult(BaseModel):
    filename: str
    status: str
    extracted_data: ExtractedData
    
class OCRResponse(BaseModel):
    doc_id: str
    message: str
