# main.py
import argparse
import logging
import time
import uuid
import os
import json
from src.config import Config
from src.fetcher import TenderFetcher
from src.parser import TenderParser
from src.cleaner import TenderCleaner
from src.storage import StorageManager

os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join("logs", "scraper.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Tender Scraper POC")
    parser.add_argument("--limit", type=int, default=Config.DEFAULT_LIMIT, help="Max tenders to scrape")
    parser.add_argument("--rate-limit", type=float, default=Config.DEFAULT_RATE_LIMIT, help="Delay between requests")
    return parser.parse_args()

def main():
    args = parse_args()

    run_metadata = {
        "run_id": str(uuid.uuid4()),
        "start_time": time.time(),
        "config": vars(args),
        "pages_visited": 0,
        "tenders_found": 0,
        "tenders_saved": 0,
        "deduped_count": 0,
        "status": "RUNNING"
    }
    
    logger.info(f"Starting Run ID: {run_metadata['run_id']}")

    try:
        fetcher = TenderFetcher(rate_limit=args.rate_limit)
        parser = TenderParser()
        cleaner = TenderCleaner()
        storage = StorageManager()

        logger.info("Fetching main listing page...")
        html = fetcher.fetch_page(Config.BASE_URL)
        run_metadata["pages_visited"] += 1

        if html:
        
            logger.info("Parsing HTML...")
            raw_tenders = parser.parse_listing(html)
            run_metadata["tenders_found"] = len(raw_tenders)
            logger.info(f"Found {len(raw_tenders)} raw items.")
          
            logger.info("Cleaning and deduplicating data...")
            cleaned_tenders = [cleaner.clean_record(t) for t in raw_tenders]
            unique_tenders = cleaner.deduplicate(cleaned_tenders)
            
            final_tenders = unique_tenders[:args.limit]
            
            run_metadata["deduped_count"] = len(raw_tenders) - len(unique_tenders)
            run_metadata["tenders_saved"] = len(final_tenders)

            storage.save_tenders(final_tenders)
            logger.info(f"Successfully saved {len(final_tenders)} tenders.")
        else:
            logger.error("No HTML content retrieved.")
            run_metadata["status"] = "FAILED_NO_CONTENT"
        
        run_metadata["status"] = "SUCCESS"

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        run_metadata["status"] = "FAILED"
        run_metadata["error"] = str(e)

    finally:
        run_metadata["end_time"] = time.time()
        run_metadata["duration_seconds"] = run_metadata["end_time"] - run_metadata["start_time"]
        
        storage.save_metadata(run_metadata)
        logger.info(f"Run {run_metadata['run_id']} completed in {run_metadata['duration_seconds']:.2f}s")

if __name__ == "__main__":
    main()