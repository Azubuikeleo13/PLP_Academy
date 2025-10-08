"""
Train a PM2.5 regressor for SDG 11 (Sustainable Cities) on the full dataset.

Primary data: "PRSA_data_2010.1.1-2014.12.31.csv"  (Beijing PM2.5, 2010–2014)
The script is resilient to network issues:
- If CSV exists under data/, it uses it.
- Else tries UCI via ucimlrepo (id=381).
- Else tries direct CSV/ZIP mirrors with 'requests'.
- Else prints clear manual-download steps and exits.

Features: TEMP, DEWP, PRES, Iws, Is, Ir, hour, month, cbwd
Target: pm2.5
Model: Pipeline( ColumnTransformer[StandardScaler, OneHotEncoder] -> RandomForestRegressor )
Metrics: MAE, RMSE, R²
Output: models/pm25_model.pkl
"""

from pathlib import Path
import io
import zipfile
import sys
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_NAME = "PRSA_data_2010.1.1-2014.12.31.csv"
DATA_PATH = DATA_DIR / CSV_NAME

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "pm25_model.pkl"

NUMERIC_FEATURES = ["TEMP", "DEWP", "PRES", "Iws", "Is", "Ir", "hour", "month"]
CATEGORICAL_FEATURES = ["cbwd"]
TARGET = "pm2.5"

# --- Column normalization helpers ---
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    low = {c: c.lower() for c in df.columns}
    df = df.rename(columns=low)

    ren = {
        "pm2_5": "pm2.5", "pm2.5": "pm2.5",
        "temp": "TEMP", "dewp": "DEWP", "pres": "PRES",
        "iws": "Iws", "is": "Is", "ir": "Ir",
        "hour": "hour", "month": "month", "cbwd": "cbwd",
        "no": "No", "year": "year", "day": "day",
    }
    df = df.rename(columns={k: v for k, v in ren.items() if k in df.columns})

    # Fallbacks
    if "pm2.5" not in df.columns:
        for c in ["pm2_5", "PM2.5", "PM2_5"]:
            if c in df.columns:
                df = df.rename(columns={c: "pm2.5"})
                break

    if "No" not in df.columns:
        df["No"] = np.arange(1, len(df) + 1)

    # Reorder (best-effort)
    preferred = ["No","year","month","day","hour","pm2.5","DEWP","TEMP","PRES","cbwd","Iws","Is","Ir"]
    ordered = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
    df = df[ordered]
    return df

# --- Data fetchers with fallbacks ---
def try_ucimlrepo():
    try:
        from ucimlrepo import fetch_ucirepo
        print("Trying UCI via ucimlrepo (id=381)...")
        ds = fetch_ucirepo(id=381)
        X = ds.data.features
        y = ds.data.targets
        df = pd.concat([X, y], axis=1)
        df = normalize_columns(df)
        return df
    except Exception as e:
        print(f"ucimlrepo fetch failed: {e}")
        return None

def http_get(url, timeout=30):
    import requests
    print(f"Downloading: {url}")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; sdg11-pm25/1.0)"}
    r = requests.get(url, headers=headers, timeout=timeout, stream=True)
    r.raise_for_status()
    return r

def try_direct_downloads():
    """
    Try a few known mirrors:
    - Raw CSV mirrors (community mirrors, educational repos)
    - UCI ZIP then extract the CSV
    We keep this best-effort and robust to offline cases.
    """
    import requests

    # 1) CSV mirrors (commonly mirrored in teaching repos)
    csv_urls = [
        # Plotly datasets mirror (commonly available)
        "https://raw.githubusercontent.com/plotly/datasets/master/PRSA_data_2010.1.1-2014.12.31.csv",
        # Public teaching mirror (fallback)
        "https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv"  # <-- placeholder; will be rejected
    ]
    for url in csv_urls:
        try:
            r = http_get(url)
            # sanity check: small wrong file stopper
            content = r.content
            # Quick guard against wrong placeholder file: require header presence
            if b"pm2.5" not in content and b"pm2_5" not in content:
                print("Downloaded file doesn't look like PM2.5 CSV; skipping this mirror.")
                continue
            with open(DATA_PATH, "wb") as f:
                f.write(content)
            print(f"Saved CSV to {DATA_PATH}")
            return pd.read_csv(DATA_PATH)
        except Exception as e:
            print(f"CSV mirror failed: {e}")

    # 2) UCI ZIP (official). We’ll download ZIP and extract the CSV.
    zip_urls = [
        # UCI archive entry — often serves a ZIP with dataset files
        "https://archive.ics.uci.edu/static/public/381/beijing+pm2.5.zip"
    ]
    for url in zip_urls:
        try:
            r = http_get(url, timeout=60)
            zf = zipfile.ZipFile(io.BytesIO(r.content))
            # Find our CSV inside the ZIP (name may match exactly or vary in case)
            names = zf.namelist()
            target = None
            for n in names:
                if n.lower().endswith(".csv") and "prsa_data_2010.1.1-2014.12.31" in n.lower():
                    target = n
                    break
            if target is None:
                # fallback: first csv inside zip
                for n in names:
                    if n.lower().endswith(".csv"):
                        target = n
                        break
            if target is None:
                raise RuntimeError("No CSV found inside ZIP.")

            with zf.open(target) as f:
                df = pd.read_csv(f)
            df = normalize_columns(df)
            df.to_csv(DATA_PATH, index=False)
            print(f"Extracted CSV to {DATA_PATH}")
            return df
        except Exception as e:
            print(f"ZIP mirror failed: {e}")

    return None

def fetch_or_load_full_dataset() -> pd.DataFrame:
    # 0) Local CSV present?
    if DATA_PATH.exists():
        print(f"Using existing local CSV: {DATA_PATH}")
        return normalize_columns(pd.read_csv(DATA_PATH))

    # 1) UCI via library
    df = try_ucimlrepo()
    if df is not None:
        df.to_csv(DATA_PATH, index=False)
        print(f"Saved full dataset to {DATA_PATH}")
        return df

    # 2) Direct mirrors (CSV / ZIP)
    df = try_direct_downloads()
    if df is not None:
        return df

    # 3) Give manual instructions and exit cleanly
    msg = f"""
    Could not download the dataset automatically (likely due to network restrictions).

    Manual fix (one-time):
      • Download the file:  PRSA_data_2010.1.1-2014.12.31.csv
      • Place it here:      {DATA_PATH.resolve()}

    Where to find it (any one of these should work in a browser):
      • UCI Machine Learning Repository page for "Beijing PM2.5"
      • Kaggle mirrors of the same dataset (search "PRSA_data_2010.1.1-2014.12.31.csv")
      • Trusted academic GitHub mirrors

    After placing the CSV, run:
      python train_model.py
    """
    print(msg)
    sys.exit(1)

# --- Training ---
def main():
    df = fetch_or_load_full_dataset()

    required = ["TEMP", "DEWP", "PRES", "Iws", "Is", "Ir", "hour", "month", "cbwd", "pm2.5"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns after normalization: {missing}")

    df = df.dropna(subset=required).copy()
    df["hour"] = df["hour"].astype(int)
    df["month"] = df["month"].astype(int)
    df["pm2.5"] = df["pm2.5"].astype(float)

    X = df[["TEMP","DEWP","PRES","Iws","Is","Ir","hour","month","cbwd"]]
    y = df["pm2.5"]

    # Stratified split via quantile bins (best-effort)
    try:
        y_bins = pd.qcut(y, q=20, labels=False, duplicates="drop")
        strat = y_bins
    except Exception:
        strat = None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=strat
    )

    pre = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), ["TEMP","DEWP","PRES","Iws","Is","Ir","hour","month"]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["cbwd"]),
        ]
    )

    model = RandomForestRegressor(
        n_estimators=500,
        random_state=42,
        n_jobs=-1,
        max_depth=None,
        min_samples_leaf=2
    )

    pipe = Pipeline([("pre", pre), ("rf", model)])
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)

    print(f"Samples used: {len(df):,}")
    print(f"MAE:  {mae:.2f} µg/m³")
    print(f"RMSE: {rmse:.2f} µg/m³")
    print(f"R²:   {r2:.3f}")

    joblib.dump(pipe, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")

if __name__ == "__main__":
    main()
