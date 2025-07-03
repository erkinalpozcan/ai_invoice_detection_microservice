FROM python:3.10-slim

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . .

CMD ["uvicorn", "yolo_detection:app", "--host", "0.0.0.0", "--port", "8000"]