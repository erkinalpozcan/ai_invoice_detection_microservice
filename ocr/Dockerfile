FROM python:3.10-slim

RUN apt-get update && apt-get install -y libgl1-mesa-glx

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["uvicorn", "ocr_service:app", "--host", "0.0.0.0", "--port", "8000"]