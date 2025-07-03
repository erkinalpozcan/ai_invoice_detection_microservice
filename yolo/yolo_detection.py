from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from ultralytics import YOLO
import io

app = FastAPI()
model = YOLO("best.pt")  

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    results = model(image, verbose=False)
    detections = []
    boxes = results[0].boxes

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = round(float(box.conf[0]), 3)
        cls_id = int(box.cls[0])
        label = model.names[cls_id]

        detections.append({
            "label": label,
            "coordinates": [x1, y1, x2, y2],
            "confidence": conf
        })

    return JSONResponse(content=detections)

