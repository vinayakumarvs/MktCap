import yfinance as yf
import pandas as pd
import time

def get_ticker_details(ticker_symbol):
    """Fetches the market cap, currency, and exchange for a given ticker symbol."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        # Fetch info once
        info = ticker.info
        market_cap = info.get('marketCap')
        currency = info.get('currency')
        exchange = info.get('exchange') # Get the exchange

        # Prepare return values, handling missing data
        ret_cap = market_cap
        ret_curr = currency.upper() if currency else None
        ret_exch = exchange if exchange else None

        if not market_cap:
            print(f"Market cap not available for {ticker_symbol}")
            ret_cap = None # Ensure cap is None if not found
        if not currency:
            print(f"Currency not available for {ticker_symbol}")
        if not exchange:
            print(f"Exchange not available for {ticker_symbol}")

        return ret_cap, ret_curr, ret_exch

    except Exception as e:
        # More specific error logging could be added here if needed
        print(f"Could not fetch data for {ticker_symbol}: {e}")
        return None, None, None

def main():
    """Reads tickers from CSV and prints their market caps, currency, and exchange."""
    try:
        # Assuming the CSV file is in the same directory as the script
        tickers_df = pd.read_csv('us_stock_tickers.csv')
        # Assuming the ticker symbols are in a column named 'Ticker'
        if 'Ticker' not in tickers_df.columns:
            print("Error: 'Ticker' column not found in us_stock_tickers.csv")
            return

        market_data = [] # Store dictionaries
        tickers_to_process = tickers_df['Ticker'].tolist()
        total_tickers = len(tickers_to_process)
        print(f"Fetching market caps, currency, and exchange for {total_tickers} tickers...")

        for i, ticker in enumerate(tickers_to_process):
            print(f"Processing {i+1}/{total_tickers}: {ticker}")
            cap, curr, exch = get_ticker_details(ticker)
            # Store data even if some parts are missing, using N/A
            market_data.append({
                'Ticker': ticker,
                'MarketCap': cap, # Keep as number or None for potential calculations
                'Currency': curr or 'N/A',
                'Market': exch or 'N/A' # Add market
            })
            # Add a small delay to avoid hitting API rate limits
            time.sleep(0.1)

        print("\n--- Market Data Results ---")
        if market_data:
            results_df = pd.DataFrame(market_data)
            # Optional: Format MarketCap for printing
            # results_df['MarketCap_Formatted'] = results_df['MarketCap'].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else 'N/A')
            print(results_df.to_string(index=False))
            # results_df.to_csv('market_data.csv', index=False)
            # print("\nResults saved to market_data.csv")
        else:
            print("No market data retrieved.")

    except FileNotFoundError:
        print("Error: us_stock_tickers.csv not found in the current directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
