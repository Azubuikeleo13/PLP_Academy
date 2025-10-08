```markdown
# Week 2 Report — AI for Sustainable Development

**Project:** PM2.5 Prediction for Sustainable Cities (SDG 11)  
**Method:** Supervised Learning (Random Forest)

## SDG Problem

PM2.5 (≤2.5 μm) drives respiratory/cardiovascular risk and degrades liveability. City managers need **fast forecasts** or **nowcasts** to alert residents and prioritize mitigation (e.g., traffic control, wet sweeping).

## ML Approach

- **Data:** Real-world subset of the UCI _Beijing PM2.5_ dataset (`data/beijing_pm25_subset.csv`).
- **Features:** Temperature, dew point, pressure, wind index, rain/snow flags, hour, month, and wind direction bucket (`cbwd`).
- **Model:** Pipeline( ColumnTransformer[StandardScaler(num), OneHotEncoder(cat)] → RandomForestRegressor ).
- **Split:** Train/test (25% test), stratified by target bins.
- **Metrics:** MAE, RMSE, R² printed after training.

## Results (demo subset)

Example output after `train_model.py`:

- MAE ≈ (varies with subset)
- RMSE ≈ (varies with subset)
- R² ≈ (varies; improves with full dataset)

Interpretation: With a tiny subset, scores vary; accuracy improves markedly with the full dataset and cross-validation.

## Impact & Use

- **Residents:** Early warnings to reduce outdoor exposure and protect sensitive groups.
- **City ops:** Time interventions and assess policies (aligns with **SDG 11** targets on air quality).

## Ethical Reflection

- **Bias & Generalization:** Training data are city/time-specific; transfer requires validation.
- **Fairness:** Provide clear uncertainty and avoid overstating precision; complement with reference-grade monitors.
- **Sustainability:** Better targeting of interventions reduces emissions and health burdens.

## Future Work

- Train on the full UCI dataset + additional cities; add lag features and rolling means.
- Compare algorithms (XGBoost, LightGBM); calibrate uncertainty.
- Add interpretability (SHAP) and a small API for ingestion from sensors/forecast data.

## Demo

Run `python app.py`, open `http://127.0.0.1:5000`, enter conditions, and view predicted PM2.5 + guidance label.
```
