# OCR Microservice

A FastAPI microservice that accepts PDF uploads, performs OCR to extract text, parses questions grouped by sections, and stores the results in MongoDB.

## Features
- **Upload Endpoint**: Accepts PDF files, runs OCR (using Tesseract), parses text, and saves to MongoDB.
- **Results Endpoint**: Retrieves parsed data by Document ID.
- **Advanced Parsing**:
  - Extracts **Questions** preserving multiline text and options.
  - Handles messy OCR output with fuzzy matching.

## Prerequisites
- **Python 3.8+**
- **MongoDB** (running locally or remote)
- **Tesseract-OCR**: Must be installed on the system.
  - Windows: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)
  - **Important**: The app looks for Tesseract in `C:\Program Files\Tesseract-OCR\tesseract.exe`.

## Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd ocr_microservice
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment (Optional)**
   - `MONGO_URI`: MongoDB connection string (default: `mongodb://localhost:27017`)
   - `DB_NAME`: Database name (default: `ocr_db`)

## Running the Service

```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

## API Usage

### 1. Upload a PDF
**Endpoint**: `POST /upload`
**Body**: `multipart/form-data` with `file` field.

**Response**:
```json
{
  "doc_id": "unique-uuid",
  "message": "File processed and stored successfully"
}
```

### 2. Get Results
**Endpoint**: `GET /results/{doc_id}`

**Response**:
```json
{
  "filename": "exam.pdf",
  "status": "processed",
  "extracted_data": {
    "sections": [
      {
        "name": "Section 1",
        "questions": [
          {
            "number": "1",
            "question": "What is the capital of France? (a) Paris (b) London"
          }
        ]
      }
    ],
    "raw_text": "..."
  }
}
```

## Assumptions
- The PDF contains selectable text or images suitable for OCR.
- Questions start with a number followed by a separator (e.g., "1.", "2)").
