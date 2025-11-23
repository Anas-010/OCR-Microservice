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

### 2. Get Results (paste the docid here from /POST)
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

## Challenges Faced
During development, we encountered and solved several key challenges:
1.  **Content Limitations**: The file `eng_1.pdf` could not be processed because it contained only answers, whereas our system is designed to extract questions.
2.  **Handwriting & Structure**: The text in some documents could not be structured correctly into the target JSON format due to handwriting issues that degraded OCR quality.
3.  **Dependency Management**: Installing external tools like Poppler on Windows is complex for users.
    *   *Solution*: We switched from `pdf2image` (requires Poppler) to `pypdfium2` (pip-installable) and added auto-detection for Tesseract paths.
4.  **Complex Parsing Logic**: Extracting questions that span multiple lines or have options, while ignoring noise.
    *   *Solution*: We developed a robust regex-based parser that groups text by numbered sections and captures full question blocks, handling typos in headers (e.g., "Seclion").

## Limitations & Notes
> [!NOTE]
> **Specific Optimization**: This microservice is specifically tuned and verified using **`2_1_1 english.pdf`**.
> It is designed primarily for **extracting numbered questions** from exam-style PDF documents. It may not perform as well on other document types (like invoices or unformatted text) without further tuning of the parser logic.

## Assumptions
- The PDF contains selectable text or images suitable for OCR.
- Questions start with a number followed by a separator (e.g., "1.", "2)").
