# TRAFFIC-PROJECT
# Machine Learning-Based Traffic Flow Prediction and Intelligent Signal Control

## Project objective

This project predicts short-term traffic flow at a road intersection and uses the predictions to support intelligent traffic signal control.

## Team

Group project — 4 members (3 CSE, 1 ECE)

- **Member 1 (this repo owner):** Data generation, preprocessing, ML prediction models
- **Member 2:** Traffic simulation (intersection, vehicle queues, signal phases)
- **Member 3:** Signal control logic and integration with ML predictions
- **Member 4:** Sensors/hardware concept, visualization, dashboards

## Initial scope

The system models a two-phase intersection:

- North-South traffic
- East-West traffic

Traffic is measured at five-minute intervals.

## Progress

- [x] GitHub repository and project structure created
- [x] Simulated traffic dataset generated and validated (17,280 rows, 60 days, 5-min intervals)
- [x] Traffic visualizations (over time, average by hour) — confirmed realistic peak patterns
- [x] Feature engineering — lag features (5/10/15/30/60 min) and rolling averages
- [x] Baseline prediction model (last-value)
- [x] Random Forest prediction model — trained and evaluated
- [x] Trained models saved (`.pkl`) and prediction function (`src/predict.py`) ready for integration
- [ ] Traffic simulation (Member 2)
- [ ] Intelligent signal controller (Member 3)
- [ ] Performance comparison: fixed-time vs. rule-based vs. ML-based control
- [ ] Final report and presentation

## Dataset columns (`data/raw/traffic_data.csv`)

| Column | Description |
| :--- | :--- |
| `timestamp` | Date and time of the observation |
| `hour` | Hour of the day |
| `minute` | Minute of the hour |
| `day_of_week` | Day number from 0 to 6 |
| `is_weekend` | 1 for weekend, otherwise 0 |
| `ns_vehicle_count` | North-South vehicles in five minutes |
| `ew_vehicle_count` | East-West vehicles in five minutes |

## Model results

Predicting traffic 5 minutes ahead, evaluated on a chronological (unseen future) test split:

| Model | Direction | MAE | RMSE | R² |
|---|---|---|---|---|
| Last-value baseline | North-South | 4.585 | 5.754 | — |
| Random Forest | North-South | **3.320** | **4.141** | **0.873** |
| Last-value baseline | East-West | 4.509 | 5.644 | — |
| Random Forest | East-West | **3.404** | **4.210** | **0.887** |

Random Forest reduces prediction error by ~27-28% over the naive baseline.

## Using the prediction model

```python
from src.predict import predict_traffic

prediction = predict_traffic(current_features_df)
# {"predicted_ns_vehicles": 35, "predicted_ew_vehicles": 12}
```

`current_features_df` must be a pandas DataFrame containing all columns listed in `models/feature_columns.pkl` (hour, minute, day_of_week, is_weekend, lag features, and rolling averages for both directions).

## Repository structure