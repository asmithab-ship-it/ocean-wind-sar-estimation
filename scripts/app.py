from fastapi import FastAPI, HTTPException, Query
import pandas as pd
import os

app = FastAPI(
    title="Ocean Wind Field Vector API",
    description="Multi-temporal SAR-derived wind fields for Tamil Nadu coastal energy planning",
    version="2.0.0"
)

# Dataset registry
DATA_REGISTRY = {
    "2025-08-15": r"C:\Users\asmit\OneDrive\Desktop\Ocean_Wind_Project\output\wind_vectors_20250815.csv",
    "2025-12-02": r"C:\Users\asmit\OneDrive\Desktop\Ocean_Wind_Project\output\wind_vectors_complete.csv"
}


@app.get("/")
def home():
    return {
        "message": "Ocean Wind Field Vector API is running",
        "available_dates": list(DATA_REGISTRY.keys())
    }


@app.get("/api/wind")
def get_wind_vectors(
    date: str = Query(..., description="Acquisition Date (YYYY-MM-DD)"),
    lat_min: float = Query(..., description="Minimum Latitude"),
    lat_max: float = Query(..., description="Maximum Latitude"),
    lon_min: float = Query(..., description="Minimum Longitude"),
    lon_max: float = Query(..., description="Maximum Longitude"),
    min_speed: float = Query(0.0, description="Minimum Wind Speed (m/s)")
):

    # Remove accidental spaces
    date = date.strip()

    # Check date
    if date not in DATA_REGISTRY:
        raise HTTPException(
            status_code=404,
            detail=f"Date {date} not available. Available dates: {list(DATA_REGISTRY.keys())}"
        )

    file_path = DATA_REGISTRY[date]

    # Check file exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=500,
            detail=f"Dataset file not found: {file_path}"
        )

    # Read CSV
    df = pd.read_csv(file_path)

    # Apply filters
    filtered_df = df[
        (df["Y"] >= lat_min) &
        (df["Y"] <= lat_max) &
        (df["X"] >= lon_min) &
        (df["X"] <= lon_max) &
        (df["speed"] >= min_speed)
    ]

    # No results
    if filtered_df.empty:
        return {
            "metadata": {
                "requested_date": date,
                "points_found": 0
            },
            "message": "No wind vectors found in selected area.",
            "data": []
        }

    # Build response
    results = []

    for _, row in filtered_df.iterrows():
        results.append({
            "id": str(row["WindField"]),
            "latitude": round(float(row["Y"]), 6),
            "longitude": round(float(row["X"]), 6),
            "speed_ms": round(float(row["speed"]), 2),
            "direction_deg": round(float(row["heading"]), 2)
        })

    return {
        "metadata": {
            "requested_date": date,
            "total_points_extracted": len(results),
            "wind_speed_min_m_s": round(float(filtered_df["speed"].min()), 2),
            "wind_speed_max_m_s": round(float(filtered_df["speed"].max()), 2)
        },
        "data": results
    }