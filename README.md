# Ocean Wind SAR Estimation using Sentinel-1 SAR Imagery

## Project Overview

This project estimates ocean surface wind fields over Indian coastal regions using Sentinel-1 Synthetic Aperture Radar (SAR) imagery. The workflow includes SAR image preprocessing, wind vector estimation, visualization using QGIS, statistical analysis, and an interactive Streamlit dashboard supported by a FastAPI backend.

---

## Features

* Sentinel-1 SAR image preprocessing
* Ocean wind field estimation
* Wind vector generation
* Interactive Streamlit dashboard
* FastAPI backend for data access
* Wind rose visualization
* Scatter plot analysis
* QGIS-based geospatial visualization

---

## Repository Structure

```
ocean-wind-sar-estimation/

├── scripts/
│   ├── api3.py
│   ├── dashboard.py
│   ├── scatterplot.py
│   └── windrose_corrected.py
│
├── data/
│   ├── wind_vectors_complete.csv
│   ├── wind_vectors_20250815.csv
│   └── validation_table.csv
│
├── output/
│   ├── August streamlit wind map.png
│   ├── august qgis.png
│   ├── december streamlit wind map.png
│   ├── december qgis.png
│   ├── scatter plot.png
│   └── windrose.png
│
├── report/
│   ├── Interim_Report.pdf
│   └── Final_Report.pdf
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Software Used

* Python
* SNAP (Sentinel Application Platform)
* QGIS
* FastAPI
* Streamlit
* Pandas
* NumPy
* Plotly
* Windrose
* SciPy

---

## Installation

Clone the repository:

```bash
git clone https://github.com/asmithab-ship-it/ocean-wind-sar-estimation.git
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Run the FastAPI Backend

```bash
uvicorn api3:app --reload
```

---

## Run the Streamlit Dashboard

```bash
streamlit run dashboard.py
```

---

## Project Outputs

The project generates:

* Ocean wind vector datasets
* Interactive Streamlit wind maps
* QGIS wind field visualizations
* Wind rose diagrams
* Scatter plot analysis
* Project reports

---

## Author

**Bhukya Asmitha 23113041 **

Department of Civil Engineering

Project: **Ocean Wind SAR Estimation using Sentinel-1 SAR Imagery**
