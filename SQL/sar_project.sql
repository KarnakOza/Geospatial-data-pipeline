CREATE EXTENSION postgis; 


CREATE TABLE sar_scenes (
    scene_id TEXT PRIMARY KEY,
    acquisition_date DATE,
    orbit_direction TEXT,
    polarization TEXT,
    footprint GEOMETRY(POLYGON, 4326)
);

CREATE TABLE port_zones (
    id SERIAL PRIMARY KEY,
    name TEXT,
    geom GEOMETRY(POLYGON, 4326)
);

CREATE TABLE ships_detected (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(POINT, 4326),
    intensity FLOAT,
    detection_date DATE
);
