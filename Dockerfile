# Use official Python image[cite: 1]
FROM python:3.11-slim

# Install system dependencies required by OpenCV (Used by YOLO)
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Set working directory[cite: 1]
WORKDIR /app

# Copy requirements and install dependencies[cite: 1]
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code
COPY . .

# Expose port (FastAPI default is 8000)[cite: 1]
EXPOSE 8000

# Update entrypoint to use uvicorn for ASGI apps[cite: 1]
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]