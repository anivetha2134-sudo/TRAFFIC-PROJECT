# Machine Learning-Based Traffic Flow Prediction and Intelligent Signal Control

## Project objective

Predict short-term traffic flow at a road intersection and use the predictions to support intelligent traffic signal control, then compare against fixed-time and rule-based control.

## Scope

A two-phase intersection (North-South and East-West), with traffic counted at 5-minute intervals. All current results use simulated data; real-data validation is pending.

## Progress

## Progress

- [x] Repository, folder structure, virtual environment
- [x] Simulated traffic dataset (60 days, 5-minute intervals)
- [x] Feature engineering (lag values, rolling averages, targets)
- [x] Baseline and Random Forest prediction models
- [x] Trained models saved, `src/predict.py` ready
- [x] Intersection simulation with fixed-time, rule-based and ML-based controllers
- [x] Multi-day and no-queue-sensor evaluation
- [x] Validation of the prediction model on real traffic data (UCI and Kaggle)
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

## Real-data validation (06_real_data.ipynb)

Next-hour prediction, chronological split (train on the earlier 80%, test on the last 20%). Missing hours were dropped, not filled.

**UCI Metro Interstate Traffic Volume** (hourly I-94 westbound, about 3,300 vehicles/hour; test period Dec 2017 - Sep 2018)

| Method | MAE | R2 |
| :--- | :--- | :--- |
| Same hour yesterday | 564.4 | 0.729 |
| Current hour | 582.9 | 0.831 |
| Same hour last week | 350.7 | 0.884 |
| Typical value for weekday and hour | 278.1 | 0.936 |
| Random Forest | 148.6 | 0.986 |

**Kaggle traffic prediction dataset** (hourly counts at 3 junctions, Nov 2015 - Jun 2017)

| Junction | Avg vehicles/hour | MAE current hour | MAE typical weekday/hour | MAE Random Forest | R2 Random Forest |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 67.2 | 6.26 | 27.51 | 4.48 | 0.926 |
| 2 | 23.7 | 2.94 | 11.76 | 3.15 | 0.742 |
| 3 | 17.5 | 3.72 | 5.98 | 3.08 | 0.698 |

Random Forest clearly beat the baselines on the high-volume highway and at junction 1, gave a modest gain at junction 3, and did not beat the current-hour baseline at junction 2. The benefit depends on traffic volume and regularity.

**Data sources (not included in this repository; download and place in `data/raw/real/`):**
- Hogue, J. (2019). Metro Interstate Traffic Volume. UCI Machine Learning Repository. https://doi.org/10.24432/C5X60B (CC BY 4.0)
- Kaggle: "Traffic Prediction Dataset" (fedesoriano). Check the dataset page for its license.

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
