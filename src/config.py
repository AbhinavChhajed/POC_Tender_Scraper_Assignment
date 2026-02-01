# src/config.py
import os

class Config:
    BASE_URL = "https://tender.nprocure.com/"
    # Default settings (can be overridden by CLI args)
    DEFAULT_LIMIT = 10
    DEFAULT_CONCURRENCY = 1
    DEFAULT_RATE_LIMIT = 2.0  # Seconds between requests
    
    # Paths
    DATA_DIR = "data"
    OUTPUT_FILE = os.path.join(DATA_DIR, "sample-output.json")
    METADATA_FILE = os.path.join(DATA_DIR, "metadata.json")
    
    # Retry Logic
    MAX_RETRIES = 3
    TIMEOUT = 30000  # 30 seconds for Playwright