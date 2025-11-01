import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from extractor import (
    extract_text_from_image
)
from extractor import analyze_pii
 
app = FastAPI(
    title="PII Extractor",
    description="Extract text using OCR and identify PII entities with Presidio",
    version="1.0"
)

@app.post("/pii_identification")
async def analyze_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    contents = await file.read()
    text = ""

    try:
        if filename.endswith((".png", ".jpg", ".jpeg")):
            text = extract_text_from_image(contents)
        elif filename.endswith(".txt"):
            text = contents.decode(errors="ignore")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {e}")

    if not text.strip():
        return {"message": "No readable text found in document."}

    pii_data = analyze_pii(text)

    return {
        "filename": filename,
        "pii_entities": pii_data,
        "preview_text": text[:300]
    }

@app.get("/")
def home():
    return {"message": "Welcome to PII Analyzer API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
