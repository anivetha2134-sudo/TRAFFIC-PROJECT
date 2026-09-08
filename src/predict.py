import joblib
import pandas as pd

ns_model = joblib.load("../models/ns_traffic_model.pkl")
ew_model = joblib.load("../models/ew_traffic_model.pkl")
feature_columns = joblib.load("../models/feature_columns.pkl")


def predict_traffic(input_data):
    """
    input_data must be a pandas DataFrame containing all feature columns:
    hour, minute, day_of_week, is_weekend, ns_lag_1...ns_lag_12,
    ew_lag_1...ew_lag_12, ns_rolling_mean_3/6, ew_rolling_mean_3/6
    """
    input_features = input_data[feature_columns]

    ns_prediction = ns_model.predict(input_features)[0]
    ew_prediction = ew_model.predict(input_features)[0]

    return {
        "predicted_ns_vehicles": max(0, round(ns_prediction)),
        "predicted_ew_vehicles": max(0, round(ew_prediction))
    }