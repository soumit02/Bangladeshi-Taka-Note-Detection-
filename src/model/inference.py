import os
from ultralytics import YOLO

def run_inference(image_path, model_path):
    """
    Runs YOLOv11 classification inference on a single image and returns the results.
    """
    # 1. Check if the image file exists
    if not os.path.exists(image_path):
        print(f"Error: The image file '{image_path}' was not found.")
        return None

    # 2. Load the trained model
    try:
        best_model = YOLO(model_path)
        print("Model loaded successfully! ✅")
    except Exception as e:
        print(f"Issue loading the model: {e}")
        return None

    print(f"\nImage loaded: {image_path}")
    print("Prediction in progress...\n")

    # 3. Make prediction
    results = best_model.predict(source=image_path, show=False, save=False)

    # 4. Process and print the results nicely
    print("=" * 40)
    print("          Prediction Results          ")
    print("=" * 40)

    predictions = []

    for r in results:
        # For classification, YOLO uses r.probs to get probabilities
        if r.probs is not None:
            # Get the class ID with the highest probability
            top_class_id = r.probs.top1
            
            # Extract confidence score and class name
            confidence = float(r.probs.top1conf)
            class_name = best_model.names[top_class_id]

            # Store results in a dictionary (useful for FastAPI)
            predictions.append({
                "class_name": class_name,
                "confidence": confidence
            })

            # Print to terminal
            print(f"💰 Detected Note: {class_name} Taka")
            print(f"📊 Confidence Score: {confidence * 100:.2f}%\n")
        else:
            print("No classification probabilities found.")

    print("=" * 40 + "\n")
    return predictions

# 5. Block to test the script directly from VS Code terminal
if __name__ == "__main__":
    # Define paths
    MODEL_PATH = "src/model/best.pt"
    TEST_IMAGE_PATH = "sample_images/images_20.jpg" 

    # Run the prediction
    run_inference(image_path=TEST_IMAGE_PATH, model_path=MODEL_PATH)