import os
import torch
from samgeo import SamGeo

def run_segmentation():
    input_tif = "data/raw/aerial_sample.tif"
    output_mask = "data/processed/sam_masks.tif"
    output_vector = "outputs/vectors/extracted_features.gpkg"
    
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("outputs/vectors", exist_ok=True)
    
    print(f"CUDA Available: {torch.cuda.is_available()}")
    print("Initializing Geo-SAM (Segment Anything Model)...")
    
    # Initialize Geo-SAM with ViT-B backbone
    sam = SamGeo(
        model_type="vit_b",
        automatic=True,
        sam_kwargs={
            "points_per_side": 32,
            "pred_iou_thresh": 0.86,
            "stability_score_thresh": 0.92,
            "min_mask_region_area": 100
        }
    )
    
    print("Segmenting objects from GeoTIFF...")
    sam.generate(input_tif, output=output_mask, foreground=True, unique=True)
    
    print(f"Vectorizing raster masks to GeoPackage format: {output_vector}")
    sam.tiff_to_gpkg(output_mask, output_vector, simplify_tolerance=0.5)
    print("Segmentation & Vectorization Complete!")

if __name__ == "__main__":
    run_segmentation()