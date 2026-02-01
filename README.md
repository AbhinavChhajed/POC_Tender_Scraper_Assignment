# POC_Tender_Scraper_Assignment

# nProcure Tender Scraper (POC)

A production-minded Proof of Concept (POC) for scraping tender data from (https://tender.nprocure.com/), featuring run-level metadata, robust error handling, and separation of concerns.

## 🚀 Features
* **Hybrid Architecture:** Uses **Playwright** for reliable dynamic content rendering (AngularJS) and **BeautifulSoup** for high-speed parsing.
* **Resilience:** Implements exponential backoff retries and explicit wait conditions for data loading.
* **Observability:** Generates a `metadata.json` audit trail for every run (duration, success counts, config used).
* **Compliance:** strictly adheres to "No Runtime LLM" constraints.

## 🛠️ Installation

1. Clone the repository:

   git clone https://github.com/AbhinavChhajed/POC_Tender_Scraper_Assignment
   cd POC_Tender_Scraper_Assignment

2. Install dependencies:

Bash
pip install -r requirements.txt
playwright install chromium

3. Usage:
Run the scraper via the command line interface (CLI):

# Scrape 50 tenders with a 2-second delay between requests
python main.py --limit 50 --rate-limit 2.0

#  Output
data/sample-output.json: The cleaned, structured tender data.

data/metadata.json: Execution logs and statistics.

logs/scraper.log: Detailed debug information.

# Project Structure
src/fetcher.py: Handles browser interaction and network logic.

src/parser.py: Extracts raw data using CSS selectors.

src/cleaner.py: Normalizes data and handles business logic.

src/storage.py: Manages file persistence.