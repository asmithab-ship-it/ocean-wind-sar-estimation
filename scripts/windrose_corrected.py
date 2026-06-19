from windrose import WindroseAxes
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(
    r"C:\Users\asmit\OneDrive\Desktop\Ocean_Wind_Project\scripts\lat log.csv"
)

# Convert -180..0 to 0..360
df["direction360"] = (df["direction"] + 360) % 360

print(df[["direction", "direction360"]].head())

# Plot wind rose
ax = WindroseAxes.from_ax()

ax.bar(
    df["direction360"],
    df["speed"],
    normed=True,
    opening=0.8,
    edgecolor="white"
)

ax.set_legend(title="Wind Speed (m/s)")

plt.title(
    "Tamil Nadu Offshore Wind Rose (Corrected Directions)"
)

plt.savefig(
    r"C:\Users\asmit\OneDrive\Desktop\Ocean_Wind_Project\output\site_windrose_corrected.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()