CREATE TABLE sar_scenes (
    id SERIAL PRIMARY KEY,
    scene_name TEXT UNIQUE,
    acquisition_date TIMESTAMP,
    orbit_direction TEXT,
    polarization TEXT,
    footprint GEOMETRY(POLYGON, 4326),
    file_path TEXT
);
