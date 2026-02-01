#### **B. `schema.md` (The Data Contract)**
*Save this as `schema.md`*

```markdown
# Data Schema Documentation

## 1. Tender Record (`tenders.json`)
The scraper outputs a list of JSON objects with the following schema:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `tender_id` | String | Unique system identifier extracted from the link or notice number. Used for deduplication. | `"271812"` |
| `notice_no` | String | The official IFB/Tender Notice Number displayed in the first column. | `"2025-26/131/15"` |
| `title` | String | The name of the work or tender title. | `"Construction of sub centre..."` |
| `organization` | String | The issuing authority or department. | `"PIU-Project Implementation Unit"` |
| `tender_type` | Enum | Categorization based on title keywords (`Works`, `Goods`, `Services`). | `"Works"` |
| `contract_value` | String | The estimated contract value. | `"7253492.00"` |
| `closing_date` | Date | Submission deadline in ISO 8601 format (`YYYY-MM-DD`). | `"2026-02-11"` |
| `publish_date` | Date | Date of scraping (Site does not explicitly list publish date on index). | `"2026-02-01"` |
| `source_url` | String | Origin URL. | `"https://tender.nprocure.com/"` |

## 2. Run Metadata (`metadata.json`)
Every execution appends a record to this file to track scraper health.

| Field | Description |
|-------|-------------|
| `run_id` | UUID v4 for tracing specific executions. |
| `start_time` / `end_time` | Unix timestamps for performance monitoring. |
| `duration_seconds` | Total execution time. |
| `config` | The CLI arguments used (e.g., limit, rate_limit). |
| `tenders_found` | Raw count of items parsed from HTML. |
| `tenders_saved` | Final count after cleaning and limiting. |
| `deduped_count` | Number of duplicate records removed. |
| `status` | `SUCCESS` or `FAILED`. |