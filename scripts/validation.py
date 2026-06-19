import pandas as pd
import xarray as xr
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

# Load SAR wind vectors
sar_df = pd.read_csv(
    r"C:\Users\asmit\OneDrive\Desktop\Ocean_Wind_Project\scripts\lat log.csv"
)

# Load ERA5 NetCDF
ds = xr.open_dataset(
    r"C:\Users\asmit\OneDrive\Desktop\Ocean_Wind_Project\scripts\data.nc"
)

# Calculate ERA5 wind speed
u = ds["u10"].values[0]
v = ds["v10"].values[0]

era5_speed_grid = np.sqrt(u**2 + v**2)

era5_lats = ds["latitude"].values
era5_lons = ds["longitude"].values

# Match each SAR point to nearest ERA5 grid point
era5_speeds = []

for _, row in sar_df.iterrows():

    lat_idx = np.abs(era5_lats - row["Y"]).argmin()
    lon_idx = np.abs(era5_lons - row["X"]).argmin()

    matched_speed = era5_speed_grid[lat_idx, lon_idx]

    era5_speeds.append(matched_speed)

sar_df["ERA5_speed"] = era5_speeds

# Calculate statistics
sar_speed = sar_df["speed"].values
era5_speed = sar_df["ERA5_speed"].values

bias = np.mean(sar_speed - era5_speed)

mae = np.mean(
    np.abs(sar_speed - era5_speed)
)

rmse = np.sqrt(
    np.mean((sar_speed - era5_speed) ** 2)
)

r, _ = pearsonr(
    sar_speed,
    era5_speed
)

r2 = r ** 2

print("\n--- VALIDATION RESULTS ---")
print(f"Bias : {bias:.3f} m/s")
print(f"MAE  : {mae:.3f} m/s")
print(f"RMSE : {rmse:.3f} m/s")
print(f"R²   : {r2:.3f}")

# Scatter plot
plt.figure(figsize=(6,6))

plt.scatter(
    era5_speed,
    sar_speed,
    alpha=0.7
)

max_val = max(
    np.max(sar_speed),
    np.max(era5_speed)
)

plt.plot(
    [0, max_val],
    [0, max_val],
    "k--"
)

plt.xlabel("ERA5 Wind Speed (m/s)")
plt.ylabel("SAR Wind Speed (m/s)")
plt.title("SAR vs ERA5 Validation")

plt.grid(True)

plt.savefig(
    r"C:\Users\asmit\OneDrive\Desktop\Ocean_Wind_Project\validation_scatter_plot.png",
    dpi=300
)

plt.show()