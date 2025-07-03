from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import pytesseract
from PIL import Image
import io
import json

app = FastAPI()

def preprocess_image(crop):
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    _, thresh = cv2.threshold(resized, 150, 255, cv2.THRESH_BINARY)
    return thresh

@app.post("/ocr")
async def ocr(
    file: UploadFile = File(...),
    detections: str = Form(...)
):
    
    try:
        detections_json = json.loads(detections)
    except Exception as e:
        return JSONResponse(content={"error": "Invalid JSON in detections"}, status_code=400)

    
    image_bytes = await file.read()
    npimg = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    if image is None:
        return JSONResponse(content={"error": "Invalid image file"}, status_code=400)

    
    for det in detections_json:
        x1, y1, x2, y2 = det["coordinates"]
        crop = image[y1:y2, x1:x2]
        processed = preprocess_image(crop)
        text = pytesseract.image_to_string(processed, config="--psm 6")
        det["text"] = text.strip().replace('\n', ' ')

    return JSONResponse(content=detections_json)
