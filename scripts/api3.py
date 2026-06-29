from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import os

# ==========================================================
# Ocean Wind Field Estimation API
# Version 3.0
# Author: Bhukya Asmitha
# ==========================================================

app = FastAPI(
    title="Ocean Wind Field Estimation API",
    description="Returns ocean wind vectors estimated from Sentinel-1 SAR datasets.",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATA_DIR = os.path.join(PROJECT_DIR, "Output for both")

DATA_REGISTRY = {
    "2025-12-02": os.path.join(DATA_DIR, "wind_vectors_complete.csv"),
    "2025-08-15": os.path.join(DATA_DIR, "wind_vectors_20250815.csv"),
}

# ==========================================================
# Load Dataset
# ==========================================================

def load_dataset(date: str):

    if date not in DATA_REGISTRY:
        raise HTTPException(
            status_code=404,
            detail=f"Dataset not available for {date}"
        )

    path = DATA_REGISTRY[date]

    if not os.path.exists(path):
        raise HTTPException(
            status_code=404,
            detail=f"CSV file not found:\n{path}"
        )

    df = pd.read_csv(path)

    # December Dataset
    if "X" in df.columns:

        df = df.rename(columns={
            "X": "longitude",
            "Y": "latitude",
            "speed": "speed_ms",
            "direction": "direction_deg"
        })

    # August Dataset
    else:

        df = df.rename(columns={
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Wind Speed (m/s)": "speed_ms",
            "Wind Direction (°)": "direction_deg"
        })

    df["direction_deg"] = df["direction_deg"] % 360

    radians = np.radians(df["direction_deg"])

    df["dx"] = (df["speed_ms"] * np.sin(radians)).round(4)
    df["dy"] = (df["speed_ms"] * np.cos(radians)).round(4)

    return df


# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
def root():

    return {
        "status": "running",
        "project": "Ocean Wind Field Estimation",
        "available_dates": list(DATA_REGISTRY.keys()),
        "docs": "/docs",
        "author": "Bhukya Asmitha"
    }
# ==========================================================
# Wind Data Endpoint
# ==========================================================

@app.get("/api/wind")
def get_wind(
    date: str = Query(..., description="Dataset date"),
    lat_min: float = Query(8.0),
    lat_max: float = Query(14.0),
    lon_min: float = Query(77.0),
    lon_max: float = Query(83.0),
    min_speed: float = Query(0.0)
):

    df = load_dataset(date)

    filtered = df[
        (df["latitude"] >= lat_min) &
        (df["latitude"] <= lat_max) &
        (df["longitude"] >= lon_min) &
        (df["longitude"] <= lon_max) &
        (df["speed_ms"] >= min_speed)
    ].copy()

    if filtered.empty:
        raise HTTPException(
            status_code=404,
            detail="No wind vectors found for the selected region."
        )

    statistics = {
        "mean_speed_ms": round(float(filtered["speed_ms"].mean()), 2),
        "max_speed_ms": round(float(filtered["speed_ms"].max()), 2),
        "min_speed_ms": round(float(filtered["speed_ms"].min()), 2),
        "mean_direction_deg": round(float(filtered["direction_deg"].mean()), 2),
        "total_points": len(filtered)
    }

    metadata = {
        "requested_date": date,
        "bounding_box": {
            "lat_min": lat_min,
            "lat_max": lat_max,
            "lon_min": lon_min,
            "lon_max": lon_max
        },
        "source": "Sentinel-1 SAR + CMOD5.n + ERA5",
        "units": {
            "speed": "m/s",
            "direction": "degrees"
        }
    }

    columns = [
        "latitude",
        "longitude",
        "speed_ms",
        "direction_deg",
        "dx",
        "dy"
    ]

    return {
        "metadata": metadata,
        "statistics": statistics,
        "data": filtered[columns].round(4).to_dict(orient="records")
    }
# ==========================================================
# Summary Endpoint
# ==========================================================

@app.get("/api/summary")
def summary(
    date: str = Query(..., description="Dataset date")
):

    df = load_dataset(date)

    return {
        "date": date,
        "total_points": len(df),
        "speed_statistics": {
            "mean": round(float(df["speed_ms"].mean()), 2),
            "maximum": round(float(df["speed_ms"].max()), 2),
            "minimum": round(float(df["speed_ms"].min()), 2),
            "standard_deviation": round(float(df["speed_ms"].std()), 2)
        },
        "direction_statistics": {
            "mean_direction": round(float(df["direction_deg"].mean()), 2)
        },
        "coverage": {
            "latitude": {
                "minimum": round(float(df["latitude"].min()), 4),
                "maximum": round(float(df["latitude"].max()), 4)
            },
            "longitude": {
                "minimum": round(float(df["longitude"].min()), 4),
                "maximum": round(float(df["longitude"].max()), 4)
            }
        }
    }


# ==========================================================
# Available Dates Endpoint
# ==========================================================

@app.get("/api/available-dates")
def available_dates():

    return {
        "available_dates": list(DATA_REGISTRY.keys()),
        "total_datasets": len(DATA_REGISTRY)
    }


# ==========================================================
# Health Check Endpoint
# ==========================================================

@app.get("/health")
def health():

    datasets = {}

    for date, path in DATA_REGISTRY.items():
        datasets[date] = os.path.exists(path)

    return {
        "status": "healthy",
        "api": "Ocean Wind Field Estimation API",
        "version": "3.0.0",
        "datasets": datasets
    }


# ==========================================================
# Startup Message
# ==========================================================

print("=" * 60)
print("Ocean Wind Field Estimation API")
print("Version : 3.0.0")
print("Author  : Bhukya Asmitha")
print("Datasets:")
for d, p in DATA_REGISTRY.items():
    print(f"  {d} -> {p}")
print("=" * 60)
