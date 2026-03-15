from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1 import fish

import threading
import time
import requests


app = FastAPI(title="Aquarium AI Backend")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Include Fish Router
app.include_router(
    fish.router,
    prefix="/api/v1/fish",
    tags=["fish"]
)


# ---------------------------------
# AUTOMATIC AI DETECTION LOOP
# ---------------------------------
def auto_detection_loop():

    while True:
        try:
            print("Running automatic fish detection...")

            requests.get(
                "http://127.0.0.1:8000/api/v1/fish/live-ai"
            )

        except Exception as e:
            print("Auto detection error:", e)

        time.sleep(10)


# Start background thread
thread = threading.Thread(
    target=auto_detection_loop,
    daemon=True
)

thread.start()