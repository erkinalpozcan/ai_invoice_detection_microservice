from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
import os
import shutil
import requests
import json

app = FastAPI()

# Klasör (ilk çalıştırmada otomatik oluşur)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ➡️  URL’leri ortam değişkeninden oku; yoksa docker‑compose servis adlarını kullan
YOLO_URL = os.getenv("YOLO_URL", "http://yolo_service:8000/predict")
OCR_URL  = os.getenv("OCR_URL",  "http://ocr_service:8000/ocr")


@app.get("/health")
async def health():
    """Kubernetes/Compose readiness probe için ufak endpoint."""
    return {"status": "ok"}


@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    """Fatura fotoğrafını al → YOLO → OCR → JSON sonuç döndür."""
    # 1. Dosyayı diske kaydet
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. YOLO servisine gönder
    with file_path.open("rb") as img:
        yolo_response = requests.post(YOLO_URL, files={"file": img})

    if yolo_response.status_code != 200:
        return JSONResponse(status_code=500, content={"error": "YOLO service failed"})

    detections = yolo_response.json()

    # 3. OCR servisine gönder
    with file_path.open("rb") as img:
        ocr_response = requests.post(
            OCR_URL,
            files={"file": img},
            data={"detections": json.dumps(detections)}
        )

    if ocr_response.status_code != 200:
        return JSONResponse(status_code=500, content={"error": "OCR service failed"})

    return JSONResponse(content=ocr_response.json())
