# Aquarium AI Monitoring System

AI-powered system for monitoring aquarium fish using computer vision, a Raspberry Pi camera, FastAPI backend, and a React dashboard.

---

## Overview

This project demonstrates how artificial intelligence can be used to monitor fish activity in an aquarium in real time.

The system captures images from a camera, sends them to an AI detection model, and displays the results on a dashboard.

The goal of this prototype is to explore computer vision techniques for automated aquatic monitoring.

---

## System Architecture

Camera (Raspberry Pi / IP Camera)
↓
FastAPI Backend
↓
AI Detection Model (Roboflow)
↓
SQL Database
↓
React Dashboard

---

## Features

• Real-time camera feed
• AI-based fish detection
• Fish count monitoring
• Detection confidence tracking
• Data logging to database
• Web dashboard for visualization

---

## Tech Stack

Backend
• FastAPI
• Python
• SQLAlchemy
• Roboflow Inference API

Frontend
• React
• JavaScript
• CSS

Infrastructure
• Raspberry Pi Camera / IP Camera
• SQL Server database

---

## Project Structure

aquarium-ai
│
├── backend
│   ├── api
│   ├── database
│   ├── services
│   └── main.py
│
├── frontend
│   └── dashboard
│       └── src
│
├── README.md
├── requirements.txt
└── .gitignore

---

## How It Works

1. The camera captures an image of the aquarium.
2. The backend sends the image to an AI detection model.
3. The model returns fish detection results.
4. Detection data is stored in the database.
5. The dashboard displays the latest results.

---

## Running the Backend

Install dependencies:

pip install -r requirements.txt

Start the FastAPI server:

uvicorn backend.main:app --reload

Backend will run on:

http://127.0.0.1:8000

---

## Running the Dashboard

Navigate to the frontend project:

cd frontend/dashboard

Install dependencies:

npm install

Start the dashboard:

npm start

---

## API Example

Latest detection endpoint:

GET /api/v1/fish/latest

Example response:

{
"camera_id": "tank_cam",
"fish_count": 6,
"confidence": 0.91
}

---

## Future Improvements

• Species classification
• Fish behavior analysis
• Water quality monitoring integration
• Mobile dashboard
• Edge AI inference on Raspberry Pi

---

## Disclaimer

This project is a prototype intended for experimentation and learning purposes.

---

## Author

Joji Mathew Joseph

---
