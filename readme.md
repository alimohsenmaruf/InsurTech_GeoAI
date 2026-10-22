# InsurTech GeoAI: Automated Parcel Risk Assessment Engine

An automated computer vision and spatial analytics microservice that ingests high-resolution aerial GeoTIFF imagery, runs zero-shot feature extraction using Meta's **Segment Anything Model (Geo-SAM)**, and calculates structural underwriting risk metrics (tree canopy overhang) using **GeoPandas** and **Shapely**.

![Dashboard](outputs/vectors/dashboard_preview.png)

## Architecture & Tech Stack
* **Containerization:** Dev Container on Apple Silicon (M4 Mac / OrbStack) with `micromamba`
* **Geospatial & Vision Stack:** `torchgeo`, `segment-geospatial` (Geo-SAM), `PyTorch`, `GDAL/PROJ`
* **Spatial Data Science:** `GeoPandas`, `Shapely`, `Rasterio`, `Rioxarray`
* **Interactive Visualization:** `leafmap`, Jupyter Lab

## Pipeline Execution
```bash
# 1. Download sample aerial imagery (San Jose, CA)
python src/download_data.py

# 2. Segment roof structures & canopy via Geo-SAM
python src/segment_features.py

# 3. Calculate spatial intersection & structural risk scores
python src/risk_engine.py