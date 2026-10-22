import geopandas as gpd

def analyze_property_risks():
    vector_path = "outputs/vectors/extracted_features.gpkg"
    output_risk_path = "outputs/vectors/parcel_risk_assessment.geojson"
    
    print("Loading extracted vector geometries...")
    gdf = gpd.read_file(vector_path)
    
    # Ensure metric CRS for accurate area calculations (e.g., UTM Zone 10N for California)
    gdf = gdf.to_crs(epsg=32610)
    
    # Calculate geometric attributes
    gdf["area_m2"] = gdf.geometry.area
    gdf["perimeter_m"] = gdf.geometry.length
    gdf["compactness"] = (4 * 3.14159 * gdf["area_m2"]) / (gdf["perimeter_m"] ** 2)
    
    # Separate structures vs canopy based on geometric profiles
    buildings = gdf[(gdf["area_m2"] >= 60) & (gdf["compactness"] >= 0.4)].copy()
    canopy = gdf[(gdf["area_m2"] < 60) | (gdf["compactness"] < 0.4)].copy()
    
    buildings["building_id"] = range(1, len(buildings) + 1)
    
    print(f"Detected {len(buildings)} structures and {len(canopy)} canopy/other polygons.")
    
    # Spatial Overlay: Find tree canopy intersecting building footprints (Tree Overhang Risk)
    overhangs = gpd.overlay(buildings, canopy, how="intersection")
    overhangs["overhang_area_m2"] = overhangs.geometry.area
    
    # Summarize risk metrics per building footprint
    overhang_summary = overhangs.groupby("building_id")["overhang_area_m2"].sum().reset_index()
    buildings = buildings.merge(overhang_summary, on="building_id", how="left")
    buildings["overhang_area_m2"] = buildings["overhang_area_m2"].fillna(0)
    
    # Compute Risk Score (0 - 100)
    buildings["overhang_ratio"] = buildings["overhang_area_m2"] / buildings["area_m2"]
    buildings["risk_score"] = (buildings["overhang_ratio"] * 100).clip(upper=100).round(1)
    
    # Export back to WGS84 for GeoJSON/Mapbox visualization
    buildings = buildings.to_crs(epsg=4326)
    buildings.to_file(output_risk_path, driver="GeoJSON")
    
    print(f"Risk Assessment Engine Complete! Exported to {output_risk_path}")
    print("\nSample Output Metrics:")
    print(buildings[["building_id", "area_m2", "overhang_area_m2", "risk_score"]].head())

if __name__ == "__main__":
    analyze_property_risks()