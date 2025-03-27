import yfinance as yf
import pandas as pd
from typing import Dict, Optional

def get_company_info(ticker_symbol: str) -> Optional[Dict]:
    """
    Get company information including ticker symbol, market, and market share.
    
    Args:
        ticker_symbol (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL')
        
    Returns:
        dict: Dictionary containing company information or None if not found
    """
    try:
        # Create a Ticker object with the symbol
        ticker = yf.Ticker(ticker_symbol)
        
        # Get company info
        info = ticker.info
        
        # Check if we got valid information
        if not info or 'symbol' not in info:
            print(f"Debug: No valid information found for ticker {ticker_symbol}")
            return None
        
        # Extract relevant information
        company_info = {
            'name': info.get('longName', ticker_symbol),
            'ticker': info.get('symbol', ticker_symbol),
            'market': info.get('market', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'currency': info.get('currency', 'USD'),
            'exchange': info.get('exchange', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A')
        }
        
        return company_info
    
    except Exception as e:
        print(f"Error getting information for ticker {ticker_symbol}: {str(e)}")
        return None

def main():
    print("Enter the stock ticker symbol (e.g., 'AAPL' for Apple, 'MSFT' for Microsoft)")
    print("Note: Use the correct ticker symbol (e.g., 'GOOGL' for Google, not 'GOOG')")
    ticker_symbol = input("Ticker symbol: ").strip().upper()
    
    info = get_company_info(ticker_symbol)
    
    if info:
        print("\nCompany Information:")
        print("-" * 50)
        print(f"Name: {info['name']}")
        print(f"Ticker Symbol: {info['ticker']}")
        print(f"Market: {info['market']}")
        print(f"Exchange: {info['exchange']}")
        print(f"Market Cap: {info['market_cap']:,.2f} {info['currency']}")
        print(f"Sector: {info['sector']}")
        print(f"Industry: {info['industry']}")
    else:
        print("\nTips to get better results:")
        print("1. Make sure the ticker symbol is correct")
        print("2. Check if the company is publicly traded")
        print("3. Try using the correct exchange suffix if needed (e.g., '.L' for London)")
        print("4. Common ticker examples:")
        print("   - AAPL (Apple)")
        print("   - MSFT (Microsoft)")
        print("   - GOOGL (Google)")
        print("   - AMZN (Amazon)")
        print("   - META (Meta/Facebook)")

if __name__ == "__main__":
    main() 