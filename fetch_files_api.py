import os
import requests
from datetime import datetime

# Constants
BASE_URL = "https://data.sec.gov/submissions/"
HEADERS = {"User-Agent": "YourName YourEmail@example.com"}
CURRENT_YEAR = datetime.now().year - 1  # Fetch filings from the previous year
# Note: Adjust the year as needed for your use case
SAVE_DIR = "10k_reports"

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_cik_list():
    """Fetch a list of CIKs from EDGAR."""
    url = "https://www.sec.gov/files/company_tickers.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def fetch_10k_filings(cik):
    """Fetch 10-K filings for a given CIK."""
    url = f"{BASE_URL}CIK{cik:010d}.json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        filings = data.get("filings", {}).get("recent", {})
        return [
            (accession, form, date)
            for accession, form, date in zip(
                filings.get("accessionNumber", []),
                filings.get("form", []),
                filings.get("filingDate", []),
            )
            if form == "10-K" and date.startswith(str(CURRENT_YEAR))
        ]
    return []

def download_filing(cik, accession_number):
    """Download a filing from EDGAR."""
    accession_number = accession_number.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{accession_number}-index.html"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        file_path = os.path.join(SAVE_DIR, f"{cik}_{accession_number}.html")
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Failed to download: {url}")

def main():
    cik_list = fetch_cik_list()
    count = 0

    for cik_info in cik_list.values():
        if count >= 10:  # Limit to 10 filings for demonstration
            break

        cik = cik_info["cik_str"]
        filings = fetch_10k_filings(int(cik))

        for accession_number, form, date in filings:
            download_filing(cik, accession_number)
            count += 1
            if count >= 10:
                break

if __name__ == "__main__":
    main()
