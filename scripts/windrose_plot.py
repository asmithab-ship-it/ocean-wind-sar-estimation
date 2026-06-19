from windrose import WindroseAxes
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    r"C:\Users\asmit\OneDrive\Desktop\Ocean_Wind_Project\scripts\lat log.csv"
)

ax = WindroseAxes.from_ax()

ax.bar(
    df["direction"],
    df["speed"],
    normed=True,
    opening=0.8,
    edgecolor="white"
)

ax.set_legend(title="Wind Speed (m/s)")

plt.title(
    "Tamil Nadu Offshore Wind Rose"
)

plt.savefig(
    r"C:\Users\asmit\OneDrive\Desktop\Ocean_Wind_Project\output\site_windrose.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()