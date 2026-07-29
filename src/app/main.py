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

SERVER_NAME = os.getenv("SERVER_NAME", "Cloud Server")
MODEL_PATH = "src/model/best.pt"

@app.post("/predict", response_model=PredictionResponse)
async def predict_note(file: UploadFile = File(...)):
    
    # 1. Validate the uploaded file format
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Invalid file format.")

    # 2. Read file bytes to generate a unique hash for caching
    file_bytes = await file.read()
    image_hash = hashlib.md5(file_bytes).hexdigest()
    cache_key = f"image_{image_hash}"

    cached_data = None
    
    # 3. Try-Except block for Redis connection to prevent crashes on cloud
    try:
        cached_data = cache.get(cache_key)
    except redis.ConnectionError:
        print("Warning: Redis is not connected. Skipping cache.")

    if cached_data:
        print(f"Cache hit for {cache_key}! Returning instantly.")
        result_data = json.loads(cached_data)
        result_data["source"] = "redis_cache"
        result_data["processed_by"] = SERVER_NAME
        return result_data
        
    print("Cache miss or Redis unavailable! Processing image with YOLO model...")
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

        # 4. Try-Except block when saving the result to Redis
        try:
            cache.set(cache_key, json.dumps(result_data))
        except redis.ConnectionError:
            pass

        return result_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)