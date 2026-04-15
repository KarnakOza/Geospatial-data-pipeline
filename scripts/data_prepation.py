import geopandas as gpd

gdf = gpd.read_file("data/raw/data.geojson")
gdf = gdf.dropna(subset=["geometry"])
gdf = gdf.to_crs(epsg=4326)
