from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests
import os

from backend.database.database import SessionLocal
from backend.database.models import FishEvent
from inference_sdk import InferenceHTTPClient


# AI Client
client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=os.getenv("ROBOFLOW_API_KEY")
)

# Camera stream
CAMERA_URL = "http://192.168.2.60:8080/shot.jpg"

router = APIRouter()


# -------------------------------
# DATABASE SESSION
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# AI DETECTION FUNCTION
# -------------------------------
def detect_fish(image_path):

    result = client.infer(
        image_path,
        model_id="platy-fish-detection/6"
    )

    return result


# -------------------------------
# LIVE AI ENDPOINT
# -------------------------------
@router.get("/live-ai")
def live_ai(db: Session = Depends(get_db)):

    image_path = "backend/frame.jpg"

    img = None

    for _ in range(5):
        try:
            response = requests.get(CAMERA_URL, timeout=5)
            img = response.content

            if img:
                break
        except Exception as e:
            print("Camera request failed:", e)

    if not img:
        return {"error": "Camera not reachable"}

    with open(image_path, "wb") as f:
        f.write(img)

    result = detect_fish(image_path)

    predictions = result.get("predictions", [])

    fish_count = len(predictions)

    confidence = 0
    if predictions:
        confidence = predictions[0].get("confidence", 0)

    # SAVE TO DATABASE
    event = FishEvent(
        camera_id="tank_cam",
        fish_count=fish_count,
        male_count=0,
        female_count=0,
        confidence=confidence,
        image_path=image_path
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return {
        "fish_count": fish_count,
        "confidence": confidence,
        "predictions": predictions
    }


# -------------------------------
# GET LATEST DETECTION
# -------------------------------
@router.get("/latest")
def get_latest_detection(db: Session = Depends(get_db)):

    detection = (
        db.query(FishEvent)
        .order_by(FishEvent.created_at.desc())
        .first()
    )

    if not detection:
        return {
            "fish_count": 0,
            "male_count": 0,
            "female_count": 0,
            "confidence": 0
        }

    return {
        "camera_id": detection.camera_id,
        "fish_count": detection.fish_count,
        "male_count": detection.male_count,
        "female_count": detection.female_count,
        "confidence": detection.confidence,
        "image_path": detection.image_path,
        "created_at": detection.created_at
    }