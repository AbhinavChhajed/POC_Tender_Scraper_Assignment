# src/storage.py
import json
import os
import logging
from src.config import Config

logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self):
        os.makedirs(Config.DATA_DIR, exist_ok=True)

    def save_tenders(self, tenders):
        """
        Saves the list of clean tender dictionaries to JSON.
        """
        try:
            with open(Config.OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(tenders, f, indent=2, ensure_ascii=False)
            logger.info(f"Successfully saved {len(tenders)} tenders to {Config.OUTPUT_FILE}")
        except Exception as e:
            logger.error(f"Failed to save tenders: {e}")

    def save_metadata(self, metadata):
        """
        Appends the run metadata to a JSON file (creating a history log).
        """
        try:
            history = []
            if os.path.exists(Config.METADATA_FILE):
                try:
                    with open(Config.METADATA_FILE, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                        if not isinstance(history, list):
                            history = [] 
                except json.JSONDecodeError:
                    history = [] 

            history.append(metadata)

            with open(Config.METADATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2)
            
            logger.info(f"Run metadata saved to {Config.METADATA_FILE}")
            
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")