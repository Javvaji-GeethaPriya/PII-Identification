import io
import pytesseract
from PIL import Image
from presidio_analyzer import AnalyzerEngine

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the Presidio Analyzer once
analyzer = AnalyzerEngine()
 
def analyze_pii(text: str):
    """Analyze text for PII entities using Presidio"""
    results = analyzer.analyze(text=text, language="en",entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "SSN"])

    pii_entities = [
        {
            "entity_type": r.entity_type,
            "start": r.start,
            "end": r.end,
            "score": round(r.score, 3),
            "snippet": text[max(0, r.start - 40): r.end + 40]
        }
        for r in results
    ]

    return pii_entities


def extract_text_from_image(file_bytes: bytes) -> str:
    """Extract text from image files using pytesseract """
    image = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(image)
