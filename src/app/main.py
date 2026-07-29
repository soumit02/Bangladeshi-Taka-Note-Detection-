import os
import shutil
import json
import hashlib
import redis
from fastapi import FastAPI, File, UploadFile, HTTPException
from src.app.schemas import PredictionResponse
from src.model.inference import run_inference

app = FastAPI(title="Bangladeshi Taka Detection API")

# Connect to the Redis container
cache = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# Get the server name from environment variables (Default is 'Unknown Server')
SERVER_NAME = os.getenv("SERVER_NAME", "Unknown Server")

# Path to the trained YOLO model
MODEL_PATH = "src/model/best.pt"

@app.post("/predict", response_model=PredictionResponse)
async def predict_note(file: UploadFile = File(...)):
    
    # 1. Validate the uploaded file format
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Invalid file format.")

    # 2. Read file bytes to generate a unique hash for caching
    file_bytes = await file.read()
    image_hash = hashlib.md5(file_bytes).hexdigest()
    
    # Create a unique cache key based on the image content
    cache_key = f"image_{image_hash}"

    # 3. Check if data exists in Redis cache
    cached_data = cache.get(cache_key)

    if cached_data:
        print(f"Cache hit for {cache_key}! Returning instantly.")
        # json.loads() converts the JSON string back to a Python dictionary[cite: 1]
        result_data = json.loads(cached_data)
        result_data["source"] = "redis_cache"
        result_data["processed_by"] = SERVER_NAME
        return result_data
        
    # 4. If cache miss, process the image with YOLO
    print("Cache miss! Processing image with YOLO model...")
    temp_file_path = f"temp_{file.filename}"

    try:
        # Save the bytes to a temporary file for YOLO to read
        with open(temp_file_path, "wb") as buffer:
            buffer.write(file_bytes)

        # Run the inference
        results = run_inference(image_path=temp_file_path, model_path=MODEL_PATH)

        if not results or len(results) == 0:
            raise HTTPException(status_code=500, detail="Model could not process.")

        best_prediction = results[0]

        # Prepare the result dictionary
        result_data = {
            "class_name": best_prediction["class_name"],
            "confidence": best_prediction["confidence"],
            "source": "yolo_model",
            "processed_by": SERVER_NAME
        }

        # Store the result in Redis[cite: 1]
        cache.set(cache_key, json.dumps(result_data))

        return result_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)