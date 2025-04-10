# fetch_sec_filings.py
import os
from datetime import datetime, timedelta
from sec_edgar_downloader import Downloader
import pandas as pd

# --- Configuration ---
# IMPORTANT: Replace with the actual list of ticker symbols you want to download reports for.
# Downloading for ALL listed companies is generally not feasible due to volume and rate limits.

# SEC EDGAR requires a user agent string identifying your requests.
# Format: CompanyName YourName YourEmail@example.com
USER_AGENT = "MyCompanyName MyName my.email@example.com" # CHANGE THIS!

# Directory to save the downloaded filings
DOWNLOAD_DIR = "sec_filings"

# CSV file containing ticker symbols
CSV_TICKER_FILE = "us_stock_tickers.csv"

# Calculate the date range (last 2 years from today)
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=2*365)

# Format dates as YYYY-MM-DD for the downloader
start_date_str = START_DATE.strftime('%Y-%m-%d')
end_date_str = END_DATE.strftime('%Y-%m-%d')
# --- End Configuration ---

def get_tickers_from_csv(file_path):
    """
    Reads a CSV file and extracts ticker symbols from the 'Ticker' column.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of ticker symbols, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        if 'Ticker' in df.columns:
            tickers = df['Ticker'].dropna().astype(str).unique().tolist()
            # Optional: Filter out potential non-standard symbols if needed
            # tickers = [t for t in tickers if t.isalpha() and len(t) <= 5]
            print(f"Read {len(tickers)} unique tickers from {file_path}")
            return tickers
        else:
            print(f"Error: 'Ticker' column not found in {file_path}")
            return None
    except FileNotFoundError:
        print(f"Error: Ticker file not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return None

def download_filings(tickers, filing_types, start_date, end_date, download_dir, user_agent):
    """
    Downloads specified SEC filings for a list of tickers within a date range.
    """
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created download directory: {download_dir}")

    # Initialize the downloader
    # The email address is crucial for EDGAR identification.
    dl = Downloader(user_agent.split(' ')[0], user_agent.split(' ')[2], download_dir)

    print(f"Starting download process for filings between {start_date} and {end_date}.")
    print(f"User Agent: {user_agent}")
    print(f"Tickers: {', '.join(tickers)}")
    print(f"Filing Types: {', '.join(filing_types)}")
    print("-" * 30)

    total_downloaded = 0
    failed_tickers = {}

    for ticker in tickers:
        print(f"\nProcessing ticker: {ticker}")
        ticker_failed_filings = []
        ticker_download_count = 0
        for filing_type in filing_types:
            try:
                # Download filings for the specific type and date range
                # Set download_details=True to get metadata about downloads
                num_downloaded = dl.get(filing_type, ticker, after=start_date, before=end_date, download_details=True)

                if num_downloaded > 0:
                    print(f"  Successfully downloaded {num_downloaded} {filing_type} filing(s) for {ticker}.")
                    ticker_download_count += num_downloaded
                else:
                    print(f"  No {filing_type} filings found for {ticker} in the specified date range.")

            except Exception as e:
                print(f"  ERROR downloading {filing_type} for {ticker}: {e}")
                ticker_failed_filings.append(filing_type)

        if ticker_failed_filings:
            failed_tickers[ticker] = ticker_failed_filings
        total_downloaded += ticker_download_count

    print("\n" + "=" * 30)
    print("Download process finished.")
    print(f"Total filings downloaded: {total_downloaded}")
    if failed_tickers:
        print("\nFailed downloads:")
        for ticker, types in failed_tickers.items():
            print(f"  - {ticker}: {', '.join(types)}")
    print("=" * 30)

if __name__ == "__main__":
    # Get tickers from CSV file
    ticker_list = get_tickers_from_csv(CSV_TICKER_FILE)

    if ticker_list:
        filing_types_to_download = ["10-K", "10-Q"]
        download_filings(
            ticker_list, # Use the list read from CSV
            filing_types_to_download,
            start_date_str,
            end_date_str,
            DOWNLOAD_DIR,
            USER_AGENT
        )
    else:
        print("Exiting: Could not retrieve ticker symbols from CSV.")