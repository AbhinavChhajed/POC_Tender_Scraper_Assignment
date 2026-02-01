# src/parser.py
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)

class TenderParser:
    def parse_listing(self, html_content):
        """
        Parses the nprocure specific table structure.
        """
        soup = BeautifulSoup(html_content, 'lxml')
        tenders = []
        
        # 1. Target the specific table by ID
        table = soup.find('table', id='DataTables_Table_0')
        if not table:
            # Fallback: Try finding any table with 'Tender Id' in it
            logger.warning("Table #DataTables_Table_0 not found by ID. Trying fallback search.")
            for t in soup.find_all('table'):
                if "Tender Id" in t.get_text():
                    table = t
                    break
        
        if not table:
            logger.error("No valid tender table found in HTML.")
            return []
            
        # 2. Iterate over rows (skip header)
        tbody = table.find('tbody')
        if not tbody:
            return []
            
        rows = tbody.find_all('tr')
        
        for row in rows:
            try:
                cols = row.find_all('td')
                if len(cols) < 2:
                    continue
                
                # --- Column 0: Notice Number ---
                notice_no = cols[0].get_text(strip=True)
                
                # --- Column 1: The "Packed" Details ---
                details_col = cols[1]
                
                # A. Extract Organization
                org_text = "Unknown"
                org_span = details_col.find('span', style=lambda s: s and 'color:#f44336' in s)
                if org_span:
                    raw_org = org_span.get_text(strip=True)
                    org_text = raw_org.split('Tender Id')[0].strip()

                # B. Extract System Tender ID
                tender_id = notice_no 
                id_link = details_col.find('a', id='tenderInProgress')
                if id_link:
                    id_text = id_link.get_text(strip=True)
                    if "Tender Id :" in id_text:
                        tender_id = id_text.split(":")[-1].strip()

                # C. Extract Title
                title = "N/A"
                title_marker = details_col.find('strong', string=re.compile("Name Of Work"))
                if title_marker and title_marker.parent:
                    full_title_text = title_marker.parent.get_text(strip=True)
                    title = full_title_text.replace("Name Of Work :", "").strip()

                # D. Extract Closing Date
                closing_date = None
                date_p = details_col.find('p', string=re.compile("Last Date"))
                if date_p:
                    date_text = date_p.get_text(strip=True)
                    match = re.search(r"(\d{1,2}-\d{1,2}-\d{4})", date_text)
                    if match:
                        closing_date = match.group(1)

                # E. Extract Estimated Value
                value = "N/A"
                val_p = details_col.find('p', style=lambda s: s and 'color:#FF9933' in s)
                if val_p:
                     val_text = val_p.get_text(strip=True)
                     if "Estimated Contract Value" in val_text:
                         value = val_text.split(":")[-1].strip()

                tenders.append({
                    "tender_id": tender_id,
                    "notice_no": notice_no,
                    "title": title,
                    "organization": org_text,
                    "closing_date": closing_date,
                    "tender_value": value,
                    "tender_type": "Works" if "Construction" in title else "Services",
                    "source_url": "https://tender.nprocure.com/"
                })

            except Exception as e:
                logger.error(f"Row parse error: {e}")
                continue
                
        return tenders