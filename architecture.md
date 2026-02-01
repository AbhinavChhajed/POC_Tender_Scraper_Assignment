# Architecture Decisions

## 1. Challenge: Dynamic Content (AngularJS)
The target site (`nprocure.com`) uses AngularJS. The HTML table structure (`<table>`) loads immediately, but the data rows (`<tr>`) are populated asynchronously via JavaScript.
* **Failed Approach:** Using `requests` returns only the table skeleton.
* **Selected Approach:** **Playwright (Python)**. It allows us to wait for specific DOM states (`page.wait_for_selector("td.sorting_1")`) ensuring data is present before parsing.

## 2. Parsing Strategy: Hybrid
While Playwright *can* extract text, it is slower at traversing the DOM than **BeautifulSoup**.
* **Workflow:** Playwright handles the network and rendering -> Passes raw HTML to BeautifulSoup -> BeautifulSoup parses data.
* **Benefit:** This decouples the "Fetching" complexity from the "Parsing" logic, making the parser easier to test with static HTML files.

## 3. Data Layout Handling
The site uses a non-standard table where Column 2 contains packed data (Organization, ID, Title, Date, Value) inside nested `<span>`, `<strong>`, and `<a>` tags.
* **Parser Logic:** The parser targets specific CSS classes (`.sorting_1`) and distinct styles (`color:#f44336` for Org, `color:#FF9933` for Value) to disentangle this data reliably.

## 4. Metadata & Observability
To meet production standards, the scraper does not just "print" data. It maintains a persistent `metadata.json` log. This allows an engineer to answer questions like:
* "Did the scraper fail last night?"
* "How long did it take to scrape 50 records?"
* "Are we seeing more duplicates than usual?"