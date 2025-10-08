# Pitch — Cleaner Air for Sustainable Cities (SDG 11)

## 1) Hook (30s)

Air you can’t see can still harm you. A quick PM2.5 predictor helps cities protect people—every hour counts.

## 2) Problem (45s)

- PM2.5 spikes drive ER visits and missed workdays.
- Cities need simple tools that translate weather/wind data into actionable alerts.

## 3) Solution (60s)

A lightweight ML model (Random Forest) predicts PM2.5 from weather + wind features, served via a minimal Flask web UI. Outputs a number **(µg/m³)** and a health label (Good/Moderate/Unhealthy…).

## 4) How it Works (60s)

- Inputs: TEMP, DEWP, PRES, wind index (Iws), rain/snow indicators, hour, month, wind direction (cbwd).
- Pipeline: Scale numeric, one-hot encode categorical → Random Forest.
- Deployed as a Flask page—easy to demo and extend.

## 5) Impact (45s)

- Residents get timely guidance; sensitive groups stay safer.
- City teams can schedule interventions (street washing, traffic measures).
- Advances SDG 11 (and supports SDG 3 & 13).

## 6) Ethics (30s)

- Advisory only; validate locally and communicate uncertainty.
- Avoid overfitting to one city; expand datasets.

## 7) Roadmap (30s)

- Train on full datasets, add lagged features & meteorology forecasts.
- Try gradient boosting; add explanations & uncertainty bands.
- Pilot with local agencies; integrate with sensor feeds.

## 8) Ask (30s)

- Data partnerships and pilot sites.
- Support for deployment/monitoring.
