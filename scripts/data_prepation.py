import geopandas as gpd

gdf = gpd.read_file("data/raw/data.geojson")
gdf = gdf.dropna(subset=["geometry"])
gdf = gdf.to_crs(epsg=4326)


import asf_search as asf

AOI = 'POLYGON((69.6475 22.7016,69.7499 22.7016,69.7499 22.7728,69.6475 22.7728,69.6475 22.7016))'

results = asf.search(
    platform=asf.PLATFORM.SENTINEL1,
    beamMode='IW',
    intersectsWith=AOI,
    start='2025-04-01',
    end='2026-04-08'
)

# keep ONLY GRDH
grdh = [r for r in results if "GRDH" in r.properties['sceneName']]

print("Number of GRDH scenes:", len(grdh))

scene_names = list(set([r.properties["sceneName"] for r in grdh]))
print(len(scene_names))

for r in grdh:
    print(r.properties['sceneName'])
