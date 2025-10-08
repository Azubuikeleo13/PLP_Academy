from flask import Flask, render_template, request
import numpy as np
import pandas as pd  # <-- use DataFrame for model input
import joblib
import re

app = Flask(__name__, static_folder="static", template_folder="templates")

MODEL_PATH = "models/pm25_model.pkl"
model = joblib.load(MODEL_PATH)

# Must match the names used in train_model.py's ColumnTransformer
NUMERIC_FEATURES = [
    "TEMP",      # °C
    "DEWP",      # °C
    "PRES",      # hPa
    "Iws",       # wind speed index
    "Is",        # snow indicator
    "Ir",        # rain indicator
    "hour",      # 0-23
    "month"      # 1-12
]
CATEGORICAL_FEATURES = ["cbwd"]  # wind direction bucket

def parse_number(text: str):
    if text is None:
        raise ValueError("empty")
    s = text.strip()
    if s == "":
        raise ValueError("empty")
    s = s.replace("−", "-")           # unicode minus → ascii
    if "," in s and "." not in s:     # decimal comma → dot
        s = s.replace(",", ".")
    # keep digits, dot, sign, exponent
    if not re.fullmatch(r"[+-]?\d*([.]\d+)?([eE][+-]?\d+)?", s):
        cleaned = re.sub(r"[^0-9eE+.\-]", "", s)
        if cleaned == "" or not re.fullmatch(r"[+-]?\d*([.]\d+)?([eE][+-]?\d+)?", cleaned):
            raise ValueError(f"not a number: {text!r}")
        s = cleaned
    return float(s)

def pm25_to_category(pm25):
    x = pm25
    if x <= 12: return "Good 😊"
    if x <= 35.4: return "Moderate 😐"
    if x <= 55.4: return "Unhealthy for Sensitive Groups 😷"
    if x <= 150.4: return "Unhealthy 🚫"
    if x <= 250.4: return "Very Unhealthy 🛑"
    return "Hazardous ☠️"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Parse numeric fields
        values = {}
        for f in NUMERIC_FEATURES:
            raw = request.form.get(f, None)
            if raw is None:
                return render_template("index.html", error=f"Missing field: {f}")
            try:
                val = parse_number(raw)
            except ValueError as ve:
                return render_template("index.html", error=f"Invalid number for '{f}': {ve}")
            values[f] = val

        # Range checks
        hour = int(round(values["hour"]))
        month = int(round(values["month"]))
        if not (0 <= hour <= 23):
            return render_template("index.html", error="Hour must be between 0 and 23.")
        if not (1 <= month <= 12):
            return render_template("index.html", error="Month must be between 1 and 12.")
        values["hour"] = hour
        values["month"] = month

        # Categorical
        cbwd = request.form.get("cbwd", "").strip()
        if cbwd == "":
            return render_template("index.html", error="Please select a wind direction (cbwd).")

        # >>> Build a ONE-ROW DataFrame with the exact training column names <<<
        cols = NUMERIC_FEATURES + CATEGORICAL_FEATURES
        row_dict = {**{k: values[k] for k in NUMERIC_FEATURES}, "cbwd": cbwd}
        df_in = pd.DataFrame([row_dict], columns=cols)

        # Predict
        y_hat = float(model.predict(df_in)[0])
        category = pm25_to_category(y_hat)

        tips = []
        if y_hat > 55.4:
            tips.append("Consider reducing outdoor activity and using certified masks.")
            tips.append("Promote low-emission transport (public transit, cycling).")
        elif y_hat > 35.4:
            tips.append("Sensitive groups should limit prolonged outdoor exertion.")
        else:
            tips.append("Air quality looks relatively good. Maintain greener travel choices.")

        pretty_inputs = {
            "TEMP (°C)": values["TEMP"],
            "DEWP (°C)": values["DEWP"],
            "PRES (hPa)": values["PRES"],
            "Iws (wind index)": values["Iws"],
            "Is (snow)": values["Is"],
            "Ir (rain)": values["Ir"],
            "Hour": values["hour"],
            "Month": values["month"],
            "Wind Dir (cbwd)": cbwd
        }

        return render_template(
            "result.html",
            prediction=f"{y_hat:.1f} µg/m³",
            category=category,
            inputs=pretty_inputs,
            tips=tips
        )

    except Exception as e:
        return render_template("index.html", error=f"Unexpected error: {e}")

if __name__ == "__main__":
    app.run(debug=True)
