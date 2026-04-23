CREATE EXTENSION postgis; 


CREATE TABLE sar_scenes (
    scene_id TEXT PRIMARY KEY,
    acquisition_date DATE,
    orbit_direction TEXT,
    polarization TEXT,
    footprint GEOMETRY(POLYGON, 4326)
);
