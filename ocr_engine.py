import pytesseract
import pypdfium2 as pdfium
import os
from typing import List

# NOTE: You might need to set the tesseract path if it's not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Auto-detect Tesseract in common Windows location
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Convert PDF to images and perform OCR on each page.
    """
    try:
        # Convert PDF to images using pypdfium2 (no Poppler required)
        pdf = pdfium.PdfDocument(pdf_path)
        
        full_text = ""
        for i, page in enumerate(pdf):
            # Render page to PIL image
            # Increase scale to 3 (approx 200-300 DPI) for better OCR accuracy
            image = page.render(scale=3).to_pil()
            
            # Basic Preprocessing: Convert to grayscale
            image = image.convert('L')
            
            # Optional: Simple thresholding if needed (can be tweaked)
            # point_fn = lambda x: 0 if x < 128 else 255
            # image = image.point(point_fn, '1')
            
            text = pytesseract.image_to_string(image)
            full_text += f"--- Page {i+1} ---\n{text}\n"
            
        return full_text
    except Exception as e:
        print(f"Error during OCR: {e}")
        raise e
