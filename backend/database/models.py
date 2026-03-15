from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FishEvent(Base):
    __tablename__ = "fish_events"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(String)
    fish_count = Column(Integer)

    male_count = Column(Integer)
    female_count = Column(Integer)

    confidence = Column(Float)
    image_path = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)