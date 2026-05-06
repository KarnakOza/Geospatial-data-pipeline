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
