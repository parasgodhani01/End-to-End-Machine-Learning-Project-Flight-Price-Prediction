# src_monitor/drift_monitor.py extract
import pandas as pd
from database import get_recent_predictions # helper to query Postgres
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

def check_drift():
    # Load your training reference
    reference_df = pd.read_csv("baseline_data.csv")
    
    # Fetch live inputs from production DB
    current_df = get_recent_predictions(limit=1000)
    
    # Run Evidently Report
    data_drift_report = Report(metrics=[DataDriftPreset()])
    data_drift_report.run(reference_data=reference_df, current_data=current_df)
    report_dict = data_drift_report.as_dict()
    
    # Extract structural drift score (e.g., Share of drifted features)
    drift_share = report_dict["metrics"][0]["result"]["share_of_drifted_features"]
    
    # Push to Prometheus or expose via a local metric endpoint
    print(f"Current drift feature share: {drift_share}")