# src/config.py
import os

class Config:
    BASE_URL = "https://tender.nprocure.com/"
    
    DEFAULT_LIMIT = 10
    DEFAULT_CONCURRENCY = 1
    DEFAULT_RATE_LIMIT = 2.0 
    
    
    DATA_DIR = "data"
    OUTPUT_FILE = os.path.join(DATA_DIR, "sample-output.json")
    METADATA_FILE = os.path.join(DATA_DIR, "metadata.json")
 
    MAX_RETRIES = 3
    TIMEOUT = 30000  