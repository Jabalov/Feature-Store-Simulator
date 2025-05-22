FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .       
# RUN pip install --no-cache-dir -r requirements.txt

COPY feature_serving/ ./feature_serving/   

CMD ["uvicorn", "feature_serving.main:app", "--host", "0.0.0.0", "--port", "8000"]
