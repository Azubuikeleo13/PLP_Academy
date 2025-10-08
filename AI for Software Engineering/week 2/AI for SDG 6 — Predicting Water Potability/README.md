# SDG 11 — PM2.5 Predictor (Real-World Dataset)

**Theme:** Machine Learning Meets the UN SDGs  
**SDG:** #11 Sustainable Cities & Communities (also supports SDG #3 Health, #13 Climate)  
**Approach:** Supervised Learning — Random Forest Regressor in a scikit-learn Pipeline

## Why this matters

Urban PM2.5 (fine particulate matter) is a key health risk. Predicting PM2.5 from readily available weather/wind signals can help cities alert residents, time street-washing, adjust traffic policies, and prioritize interventions.

## Dataset (real world)

- **UCI Beijing PM2.5 Dataset** (Zhang et al., 2017). We include a small subset in `data/beijing_pm25_subset.csv` for quick local training.  
  Replace it with the full dataset later for better accuracy.

## What’s inside

- `train_model.py` — trains the model and saves `models/pm25_model.pkl`
- `app.py` — Flask app serving a static page to collect inputs and display predicted PM2.5 + health guidance
- `templates/` + `static/` — simple UI
- `data/beijing_pm25_subset.csv` — real measurement subset
- `REPORT.md` — 1-page summary for submission
- `PITCH_DECK.md` — 5-minute pitch outline
- `requirements.txt` — dependencies

## Quickstart

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
python train_model.py
python app.py
# open http://127.0.0.1:5000


Result page showing predicted µg/m³ and category

Ethics & limitations
Model is advisory: Not a replacement for regulatory-grade monitoring.

Bias & domain shift: Trained on one city/time; generalization to other cities requires retraining/validation.

Transparency: Pipeline and features are documented; consider SHAP for explanations in future work.
```
