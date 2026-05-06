import asf_search as asf
import psycopg2
import time

# -------------------------------
# CONFIG
# -------------------------------
AOI = 'POLYGON((69.6475 22.7016,69.7499 22.7016,69.7499 22.7728,69.6475 22.7728,69.6475 22.7016))'

START_DATE = '2025-04-01'
END_DATE = '2026-04-08'

DOWNLOAD_PATH = r"H:\GEOSPATIAL_PIPELINE\raw_sar"

DB_CONFIG = {
    "dbname": "sar_pipeline",
    "user": "postgres",
    "password": "2026#23",
    "host": "localhost",
    "port": "5432"
}


# -------------------------------
# STEP 1 — SAFE ASF SEARCH (retry)
# -------------------------------
def safe_search(max_retries=5, delay=5):
    for attempt in range(max_retries):
        try:
            print(f"🔎 ASF Search attempt {attempt+1}...")

            results = asf.search(
                platform=asf.PLATFORM.SENTINEL1,
                beamMode='IW',
                intersectsWith=AOI,
                start=START_DATE,
                end=END_DATE
            )

            return results
            except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed: {e}")
            time.sleep(delay)

    raise Exception("❌ ASF search failed after retries")


# -------------------------------
# STEP 2 — FILTER + DEDUP
# -------------------------------
def process_results(results):
    grdh = [r for r in results if "GRDH" in r.properties['sceneName']]

    unique_dict = {r.properties["sceneName"]: r for r in grdh}
    unique_scenes = list(unique_dict.values())

    print(f"📦 Total GRDH: {len(grdh)}")
    print(f"📦 Unique scenes: {len(unique_scenes)}")

    return unique_scenes


# -------------------------------
# STEP 3 — CONNECT DB
# -------------------------------
def connect_db():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn, conn.cursor()


# -------------------------------
# STEP 4 — INSERT INTO POSTGIS
# -------------------------------
def insert_scenes(cur, scenes, limit=3):
    inserted = 0

    for i, r in enumerate(scenes[:limit], start=1):
        props = r.properties

        scene_name = props["sceneName"]
        acquisition_date = props["startTime"]
        orbit_direction = props["flightDirection"]
        polarization = props["polarization"]

        # Convert geometry to WKT
        coords = r.geometry["coordinates"][0]
        footprint = "POLYGON((" + ", ".join([f"{x} {y}" for x, y in coords]) + "))"

        file_path = f"{DOWNLOAD_PATH}\\{scene_name}.zip"

        try:
            cur.execute("""
                INSERT INTO sar_scenes 
                (scene_name, acquisition_date, orbit_direction, polarization, footprint, file_path)
                VALUES (%s, %s, %s, %s, ST_GeomFromText(%s, 4326), %s)
                ON CONFLICT (scene_name) DO NOTHING;
            """, (
                scene_name,
                acquisition_date,
                orbit_direction,
                polarization,
                footprint,
                file_path
            ))

            print(f"✅ [{i}] Inserted: {scene_name}")
            inserted += 1

        except Exception as e:
            print(f"❌ Failed insert {scene_name}: {e}")

    return inserted


# -------------------------------
# MAIN PIPELINE
# -------------------------------
def main():
    print("🚀 Starting SAR ingestion pipeline...")

    # Step 1 — Search
    results = safe_search()

    # Step 2 — Process
    unique_scenes = process_results(results)

    # Step 3 — DB
    conn, cur = connect_db()

    # Step 4 — Insert
    inserted = insert_scenes(cur, unique_scenes, limit=len(unique_scenes))

    # Step 5 — Commit
    conn.commit()
    cur.close()
    conn.close()

    print(f"\n🎯 Done. Inserted {inserted} scenes into PostGIS.")


if __name__ == "__main__":
    main()
