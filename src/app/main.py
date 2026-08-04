import os
import shutil
import json
import hashlib
import redis
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from src.app.schemas import PredictionResponse
from src.model.inference import run_inference

app = FastAPI(title="Bangladeshi Taka Detection API")

# Connect to the Redis container
cache = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

SERVER_NAME = os.getenv("SERVER_NAME", "Cloud Server")
MODEL_PATH = "src/model/best.pt"

# ==========================================
# Route for Frontend UI
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bangladeshi Taka Detector</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f3f4f6; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; }
            .navbar { width: 100%; background-color: #006a4e; padding: 15px 20px; text-align: center; color: white; position: fixed; top: 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); max-width: 450px; width: 90%; text-align: center; margin-top: 80px; }
            h2 { color: #333; margin-bottom: 5px; }
            p.subtitle { color: #666; font-size: 14px; margin-bottom: 25px; }
            
            .upload-area { border-radius: 8px; cursor: pointer; margin-bottom: 20px; transition: 0.3s; background-color: #fafafa; }
            .upload-area:hover { background-color: #e6f0ed; }
            .upload-area p { color: #006a4e; font-weight: bold; margin: 0; }
            input[type="file"] { display: none; }
            
            #preview { max-width: 100%; max-height: 200px; margin-top: 15px; display: none; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            
            .btn-predict { background-color: #006a4e; color: white; border: none; padding: 12px 24px; border-radius: 6px; font-size: 16px; cursor: pointer; width: 100%; font-weight: bold; transition: 0.3s; }
            .btn-predict:hover { background-color: #004c38; }
            .btn-predict:disabled { background-color: #9ca3af; cursor: not-allowed; }
            
            #result-card { margin-top: 25px; padding: 20px; border-radius: 8px; display: none; background-color: #f8fafc; border: 1px solid #e2e8f0; text-align: left; }
            .result-item { margin: 8px 0; font-size: 15px; color: #475569; border-bottom: 1px solid #e2e8f0; padding-bottom: 5px;}
            .result-item span { font-weight: bold; color: #0f172a; float: right;}
            
            .docs-btn { display: inline-block; margin-top: 25px; color: #2563eb; text-decoration: none; font-weight: bold; font-size: 14px; transition: 0.2s;}
            .docs-btn:hover { color: #1d4ed8; text-decoration: underline; }
            
            #loader { display: none; margin-top: 15px; color: #006a4e; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h2>Bangladeshi Bank Note Detection </h2>
        </div>

        <div class="container">
            <h2>Upload Bangladeshi Bank Note</h2>
            <p class="subtitle">Supports 10, 20, 50, 100, 200, 500, and 1000 Taka notes.</p>
            
            <label class="upload-area" id="drop-area">
                <p>📸 Click to Browse Image</p>
                <input type="file" id="fileInput" accept=".jpg, .jpeg, .png" onchange="previewImage(event)">
                <img id="preview" alt="Image Preview">
            </label>
            
            <button class="btn-predict" id="predictBtn" onclick="uploadAndPredict()">Detect Note</button>
            <div id="loader">Processing... Please wait ⏳</div>

            <div id="result-card">
                <div class="result-item">Detected Note: <span id="res-class" style="color: #006a4e; font-size: 18px;">-</span></div>
                <div class="result-item">Confidence Score: <span id="res-conf">-</span></div>
                <div class="result-item">Source: <span id="res-source">-</span></div>
                <div class="result-item">Processed By: <span id="res-server">-</span></div>
            </div>

            <a href="/docs" class="docs-btn">⚙️ Open Developer API Docs (Swagger UI)</a>
        </div>

        <script>
            // Function to show image preview
            function previewImage(event) {
                const reader = new FileReader();
                reader.onload = function(){
                    const output = document.getElementById('preview');
                    output.src = reader.result;
                    output.style.display = 'block';
                };
                if(event.target.files[0]){
                    reader.readAsDataURL(event.target.files[0]);
                }
            }

            // Function to send API request and handle response
            async function uploadAndPredict() {
                const fileInput = document.getElementById('fileInput');
                if(!fileInput.files[0]) {
                    alert("Please select an image first!");
                    return;
                }

                const formData = new FormData();
                formData.append('file', fileInput.files[0]);

                const btn = document.getElementById('predictBtn');
                const loader = document.getElementById('loader');
                const resultCard = document.getElementById('result-card');

                btn.disabled = true;
                loader.style.display = 'block';
                resultCard.style.display = 'none';

                try {
                    // Sending POST request to the /predict endpoint
                    const response = await fetch('/predict', {
                        method: 'POST',
                        body: formData
                    });

                    if(!response.ok) {
                        throw new Error("API Error or Invalid Image");
                    }

                    const data = await response.json();
                    
                    // Displaying the result in the UI
                    document.getElementById('res-class').innerText = data.class_name + " Taka";
                    document.getElementById('res-conf').innerText = (parseFloat(data.confidence) * 100).toFixed(2) + "%";
                    document.getElementById('res-source').innerText = data.source === 'redis_cache' ? '⚡ Redis Cache' : '🧠 YOLO Model';
                    document.getElementById('res-server').innerText = data.processed_by;
                    
                    resultCard.style.display = 'block';
                } catch (error) {
                    alert("Error: " + error.message);
                } finally {
                    btn.disabled = false;
                    loader.style.display = 'none';
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

# ==========================================
# Core Prediction Logic (Completely unchanged)
# ==========================================
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