from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Wind Estimation API")

DATA_REGISTRY = {
    "2025-12-02": r"C:\Users\asmit\OneDrive\Desktop\Ocean_Wind_Project\Output for both\wind_vectors_complete.csv",
    "2025-08-15": r"C:\Users\asmit\OneDrive\Desktop\Ocean_Wind_Project\Output for both\wind_vectors_20250815.csv"
}

@app.get("/")
def home():
    return {"message": "API Running"}

@app.get("/api/wind")
def get_wind(
    date: str,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    min_speed: float = 0
):

    df = pd.read_csv(DATA_REGISTRY[date])

    # December file
    if "X" in df.columns:

        df = df.rename(
            columns={
                "X": "longitude",
                "Y": "latitude",
                "speed": "speed_ms",
                "direction": "direction_deg"
            }
        )

    # August file
    else:

        print(df.columns)

        df = df.rename(
            columns={
                "Latitude": "latitude",
                "Longitude": "longitude",
                "Wind Speed (m/s)": "speed_ms",
                "Wind Direction (°)": "direction_deg"
            }
        )

    filtered = df[
        (df["latitude"] >= lat_min) &
        (df["latitude"] <= lat_max) &
        (df["longitude"] >= lon_min) &
        (df["longitude"] <= lon_max) &
        (df["speed_ms"] >= min_speed)
    ]

    return {
        "metadata": {
            "requested_date": date,
            "total_points": len(filtered)
        },
        "data": filtered.to_dict(orient="records")
    }