import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/flight_monitoring")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    features_json = Column(Text, nullable=False)
    predicted_price = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)

def save_prediction_to_db(features: dict, prediction: float):
    db = SessionLocal()
    try:
        log_entry = PredictionLog(
            features_json=json.dumps(features),
            predicted_price=prediction
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        print(f"Database sync logging error: {e}")
    finally:
        db.close()