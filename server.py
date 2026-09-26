from fastapi import FastAPI, UploadFile, File, Form
from ultralytics import YOLO
import PIL.Image
import io
import base64
import os

app = FastAPI(title="Pest & Disease Detection API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load both model versions into memory
PATH_V1 = os.path.join(BASE_DIR, "best_v1.pt")
PATH_V2 = os.path.join(BASE_DIR, "best_v2.pt")

models = {}

# Load Model v1
if os.path.exists(PATH_V1):
    models["v1"] = YOLO(PATH_V1)
    print("LOADED MODEL V1:", PATH_V1)

# Load Model v2
if os.path.exists(PATH_V2):
    models["v2"] = YOLO(PATH_V2)
    print("LOADED MODEL V2:", PATH_V2)

print("=" * 50)
print("AVAILABLE MODELS:", list(models.keys()))
print("=" * 50)

@app.get("/")
def root():
    return {
        "status": "Dual Model Pest Detection API is active",
        "available_models": list(models.keys())
    }

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    model_version: str = Form("v2"),
    conf: float = Form(0.15)
):
    if not models:
        return {"error": "No models loaded on server."}

    # Select requested model or fallback to first loaded model
    selected_model = models.get(model_version, list(models.values())[0])
    
    contents = await file.read()
    image = PIL.Image.open(io.BytesIO(contents)).convert("RGB")
    
    results = selected_model(image, conf=conf, iou=0.5)
    
    detections = []
    annotated_img = image # fallback

    for r in results:
        im_bgr = r.plot()
        im_rgb = im_bgr[..., ::-1] # Fix blue color tint
        annotated_img = PIL.Image.fromarray(im_rgb)
        
        for box in r.boxes:
            cls_id = int(box.cls[0])
            name = selected_model.names[cls_id]
            confidence = float(box.conf[0])
            detections.append({
                "pest_name": name,
                "confidence": round(confidence, 2)
            })

    buffered = io.BytesIO()
    annotated_img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return {
        "model_used": model_version,
        "pest_count": len(detections),
        "detections": detections,
        "annotated_image": img_str
    }