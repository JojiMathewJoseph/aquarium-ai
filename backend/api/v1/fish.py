from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests

from backend.database.database import SessionLocal
from backend.database.models import FishEvent
from inference_sdk import InferenceHTTPClient


import os
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
# AI DETECTION FUNCTION
# -------------------------------
def detect_fish(image_path):

    result = client.infer(
        image_path,
        model_id="platy-fish-detection/6"
    )

    return result


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
# LIVE AI ENDPOINT
# -------------------------------
@router.get("/live-ai")
def live_ai():

    print("STEP 1 - endpoint reached")

    image_path = "backend/frame.jpg"

    print("STEP 2 - requesting camera")

    img = None

    for _ in range(5):
        try:
            response = requests.get(CAMERA_URL, timeout=5)
            img = response.content

            if img:
                break
        except Exception as e:
            print("Camera request failed:", e)

    print("STEP 3 - camera image received")

    with open(image_path, "wb") as f:
        f.write(img)

    print("STEP 4 - running model")

    result = detect_fish(image_path)

    print("STEP 5 - result returned")

    fish_count = len(result["predictions"])

    return {
        "fish_count": fish_count,
        "predictions": result["predictions"],
        "image": result["image"]
    }


# -------------------------------
# SAVE DETECTION
# -------------------------------
@router.post("/detection")
def create_detection(
    camera_id: str,
    fish_count: int,
    confidence: float,
    image_path: str,
    db: Session = Depends(get_db),
):

    event = FishEvent(
        camera_id=camera_id,
        fish_count=fish_count,
        confidence=confidence,
        image_path=image_path,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return {"status": "saved", "id": event.id}


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
        return {"fish_count": 0, "confidence": 0}

    return {
        "camera_id": detection.camera_id,
        "fish_count": detection.fish_count,
        "confidence": detection.confidence,
        "image_path": detection.image_path,
        "created_at": detection.created_at,
    }