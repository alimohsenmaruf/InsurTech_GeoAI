import os
import sys

# Ensure PROJ and GDAL know where their database files live inside conda
conda_env_path = os.path.dirname(os.path.dirname(sys.executable))
os.environ["PROJ_LIB"] = os.path.join(conda_env_path, "share", "proj")
os.environ["GDAL_DATA"] = os.path.join(conda_env_path, "share", "gdal")

import leafmap

def download_sample_data():
    os.makedirs("data/raw", exist_ok=True)
    output_tif = "data/raw/aerial_sample.tif"
    
    # Bounding box covering a high-density suburban area (San Jose, CA)
    # [min_lon, min_lat, max_lon, max_lat]
    bbox = [-121.8885, 37.3312, -121.8825, 37.3362]
    
    print("Downloading high-resolution aerial GeoTIFF sample...")
    leafmap.map_tiles_to_geotiff(
        output=output_tif,
        bbox=bbox,
        zoom=18,
        source="Satellite",
        overwrite=True
    )
    print(f"Sample data saved successfully to {output_tif}")

if __name__ == "__main__":
    download_sample_data()