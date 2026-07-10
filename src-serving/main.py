import time
import os
import joblib
import pandas as pd
from fastapi import FastAPI, BackgroundTasks, HTTPException
from prometheus_client import Counter, Histogram, make_asgi_app

from schemas import FlightInferenceInput
from database import save_prediction_to_db

app = FastAPI(title="Flight Price Production Service")

REQUEST_COUNTER = Counter("model_predictions_total", "Total served inference runs")
LATENCY_HISTOGRAM = Histogram(
    "model_inference_latency_seconds",
    "Inference latency tracking spectrum",
    buckets=[0.002, 0.005, 0.01, 0.025, 0.05, 0.1, 0.5]
)

# Load model pipeline from mounted root
MODEL_PATH = os.getenv("MODEL_PATH", "/app/model.joblib")
MODEL_PIPELINE = joblib.load(MODEL_PATH)

app.mount("/metrics", make_asgi_app())

@app.post("/predict")
def predict_flight_price(payload: FlightInferenceInput, background_tasks: BackgroundTasks):
    start_time = time.time()
    REQUEST_COUNTER.inc()
    
    try:
        raw_data = payload.dict()
        input_df = pd.DataFrame([raw_data])
        
        # Core low-latency machine learning prediction
        prediction = MODEL_PIPELINE.predict(input_df)[0]
        
        duration = time.time() - start_time
        LATENCY_HISTOGRAM.observe(duration)
        
        # Offloads the slower SQL log out of the critical response path
        background_tasks.add_task(save_prediction_to_db, raw_data, float(prediction))
        
        return {
            "status": "success",
            "predicted_price": round(float(prediction), 2),
            "latency_ms": round(duration * 1000, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")