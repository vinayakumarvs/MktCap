# get_us_tickers.py
import pandas as pd
import os
from io import StringIO

# URLs for NASDAQ symbol directories (pipe-delimited text files)
NASDAQ_LISTED_URL = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
OTHER_LISTED_URL = "ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt"

# Output CSV file name
OUTPUT_CSV_FILE = "us_stock_tickers.csv"

def fetch_and_save_tickers(nasdaq_url, other_url, output_file):
    """
    Fetches ticker symbols and company names from NASDAQ FTP site
    and saves them to a CSV file.
    """
    print(f"Fetching data from {nasdaq_url} and {other_url}...")

    all_tickers_df = pd.DataFrame()

    for url in [nasdaq_url, other_url]:
        try:
            # Use StringIO to handle the text data directly
            # Need to skip the last line which is a file creation timestamp
            # Use 'latin-1' encoding as sometimes these files have non-utf8 chars
            df = pd.read_csv(
                url,
                sep='|',
                encoding='latin-1',
                skipfooter=1, # Skip the trailer line
                engine='python' # Needed for skipfooter
            )

            # Filter out test symbols and non-common stock entries if possible
            # NASDAQ files have a 'Test Issue' column (Y/N)
            if 'Test Issue' in df.columns:
                df = df[df['Test Issue'] == 'N']

            # Select and rename relevant columns
            # Column names are 'Symbol' and 'Security Name'
            if 'Symbol' in df.columns and 'Security Name' in df.columns:
                df_filtered = df[['Symbol', 'Security Name']].copy()
                df_filtered.rename(columns={'Symbol': 'Ticker', 'Security Name': 'Company Name'}, inplace=True)

                # Append to the main dataframe
                all_tickers_df = pd.concat([all_tickers_df, df_filtered], ignore_index=True)
            else:
                print(f"Warning: Could not find 'Symbol' or 'Security Name' columns in {url}")

        except Exception as e:
            print(f"Error fetching or processing data from {url}: {e}")
            # Continue to the next URL if one fails

    if not all_tickers_df.empty:
        # Remove potential duplicates (e.g., if a symbol is listed in both files somehow)
        all_tickers_df.drop_duplicates(subset=['Ticker'], inplace=True)

        # Clean up company names (remove common suffixes like Inc, Corp, Ltd etc. if desired - optional)
        # Example: all_tickers_df['Company Name'] = all_tickers_df['Company Name'].str.replace(r'\s+(Inc|Corp|Ltd|LLC)\.?$', '', regex=True)

        # Sort by ticker symbol
        all_tickers_df.sort_values(by='Ticker', inplace=True)

        # Save to CSV
        try:
            all_tickers_df.to_csv(output_file, index=False)
            print(f"Successfully saved {len(all_tickers_df)} tickers to {output_file}")
        except Exception as e:
            print(f"Error saving data to {output_file}: {e}")
    else:
        print("No ticker data was successfully fetched or processed.")

if __name__ == "__main__":
    fetch_and_save_tickers(NASDAQ_LISTED_URL, OTHER_LISTED_URL, OUTPUT_CSV_FILE)
