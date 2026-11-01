# Machine Learning-Based Traffic Flow Prediction and Intelligent Signal Control

## Project objective

Predict short-term traffic flow at a road intersection and use the predictions to support intelligent traffic signal control, then compare against fixed-time and rule-based control.

## Scope

A two-phase intersection (North-South and East-West), with traffic counted at 5-minute intervals. All current results use simulated data; real-data validation is pending.

## Progress

- [x] Repository, folder structure, virtual environment
- [x] Simulated traffic dataset (60 days, 5-minute intervals)
- [x] Feature engineering (lag values, rolling averages, targets)
- [x] Baseline and Random Forest prediction models
- [x] Trained models saved, `src/predict.py` ready
- [x] Intersection simulation with fixed-time, rule-based and ML-based controllers
- [x] Multi-day and no-queue-sensor evaluation
- [ ] Validation on real traffic data
- [ ] YOLO vehicle-counting demo
- [ ] Arduino hardware prototype
- [ ] Streamlit dashboard

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

## Model results (5-minute-ahead prediction, chronological test split)

| Model | Direction | MAE | RMSE | R2 |
| :--- | :--- | :--- | :--- | :--- |
| Baseline (current value) | North-South | 4.498 | 5.641 | 0.765 |
| Random Forest | North-South | 3.329 | 4.170 | 0.871 |
| Baseline (current value) | East-West | 4.587 | 5.749 | 0.790 |
| Random Forest | East-West | 3.411 | 4.213 | 0.887 |

## Signal control results

Average waiting time per vehicle, busy traffic, averaged over 3 unseen simulated days.

| Scenario | Fixed-time | Rule-based | Count-based | ML-based |
| :--- | :--- | :--- | :--- | :--- |
| With queue sensors | 83.78 s | 17.15 s | - | 17.26 s |
| No queue sensors | 85.93 s | - | 34.83 s | 39.72 s |

Adaptive control greatly reduced waiting time compared with fixed-time. ML prediction did not give a measurable benefit over simpler adaptive rules in this simulation.

## Using the prediction model

```python
from predict import predict_traffic

prediction = predict_traffic(current_features_df)
# {"predicted_ns_vehicles": 35, "predicted_ew_vehicles": 12}
```

`current_features_df` must be a one-row pandas DataFrame with the columns listed in `models/feature_columns.pkl`. Model paths are relative, so run from the `notebooks/` or `src/` folder.

## Repository structure

```text
TRAFFIC-PROJECT/
├── data/
│   ├── raw/                 # simulated traffic dataset
│   └── processed/           # dataset with lag/rolling features and targets
├── notebooks/
│   ├── 01_generate_and_explore_data.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_train_models.ipynb
│   ├── 04_traffic_simulation.ipynb
│   └── 05_improved_simulation.ipynb
├── src/
│   └── predict.py
├── models/                  # trained models (.pkl)
├── results/                 # graphs and result tables
├── requirements.txt
└── README.md
```

## How to run

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
jupyter notebook
```

Run the notebooks in order (01 to 05).

## Limitations

- All data is simulated, so performance on real traffic may differ.
- One intersection with two signal phases.
- Waiting time is estimated as total queue-seconds divided by vehicles arrived.
- Results come from three simulated test days.
