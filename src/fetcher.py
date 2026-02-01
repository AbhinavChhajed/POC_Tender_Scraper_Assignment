# src/fetcher.py
import time
import logging
from playwright.sync_api import sync_playwright
from src.config import Config

logger = logging.getLogger(__name__)

class TenderFetcher:
    def __init__(self, headless=True, rate_limit=Config.DEFAULT_RATE_LIMIT):
        self.headless = headless
        self.rate_limit = rate_limit

    def fetch_page(self, url):
        """
        Launches browser, navigates to URL, and returns raw HTML.
        Includes robust waiting for AngularJS tables.
        """
        logger.info(f"Fetching URL: {url}")
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = context.new_page()

            attempt = 0
            while attempt < Config.MAX_RETRIES:
                try:
                    # Respect Rate Limit
                    time.sleep(self.rate_limit)
                    
                    # Navigate
                    page.goto(url, timeout=Config.TIMEOUT, wait_until="domcontentloaded")
                    
                    # --- CRITICAL FIX: Wait for DATA rows, not just the table ---
                    # We wait for the class 'sorting_1' which appears in the first column of populated rows
                    try:
                        page.wait_for_selector("td.sorting_1", timeout=15000)
                        logger.info("Data table rows detected.")
                    except:
                        logger.warning("Timeout waiting for specific data rows. Saving whatever is present.")
                    
                    content = page.content()
                    browser.close()
                    return content

                except Exception as e:
                    attempt += 1
                    logger.warning(f"Attempt {attempt} failed for {url}: {e}")
                    time.sleep(2 ** attempt) # Exponential backoff
            
            browser.close()
            logger.error(f"Failed to fetch {url} after {Config.MAX_RETRIES} attempts")
            return None