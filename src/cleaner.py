# src/cleaner.py
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TenderCleaner:
    def __init__(self):
        pass

    def normalize_date(self, date_str):
        """
        Input: '11-02-2026' or '11-02-2026 18:00:00'
        Output: '2026-02-11' (ISO 8601)
        """
        if not date_str:
            return None
        
        try:
            # Try parsing with time first
            dt = datetime.strptime(date_str, "%d-%m-%Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
            
        return date_str # Return original if parse fails

    def normalize_type(self, title):
        """
        Heuristic to guess type based on title keywords.
        """
        title_lower = title.lower()
        if any(x in title_lower for x in ['construction', 'road', 'building', 'repair', 'civil']):
            return "Works"
        elif any(x in title_lower for x in ['supply', 'purchase', 'procurement', 'equipment']):
            return "Goods"
        elif any(x in title_lower for x in ['service', 'consultancy', 'manpower', 'hiring']):
            return "Services"
        return "Works" # Default to Works for nprocure as it's mostly infra

    def clean_record(self, raw_record):
        cleaned = {
            "tender_id": raw_record.get("tender_id", "N/A"),
            "title": raw_record.get("title", "").strip(),
            "tender_type": self.normalize_type(raw_record.get("title", "")),
            "publish_date": datetime.today().strftime('%Y-%m-%d'), # Site doesn't show publish date on listing
            "closing_date": self.normalize_date(raw_record.get("closing_date", "")),
            "organization": raw_record.get("organization", "").strip(),
            "description": raw_record.get("title", "").strip(), # Use title as desc
            "source_url": raw_record.get("source_url", ""),
            "contract_value": raw_record.get("tender_value", "0")
        }
        return cleaned

    def deduplicate(self, tenders):
        seen_ids = set()
        unique_tenders = []
        for t in tenders:
            tid = t.get("tender_id")
            if tid and tid not in seen_ids:
                seen_ids.add(tid)
                unique_tenders.append(t)
        return unique_tenders