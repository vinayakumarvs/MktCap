import yfinance as yf
from fuzzywuzzy import fuzz
from typing import List, Dict, Tuple
import pandas as pd
import requests
import json

def search_companies(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search for companies using fuzzy matching on company names.
    
    Args:
        query (str): Company name or partial name to search for
        max_results (int): Maximum number of results to return
        
    Returns:
        List[Dict]: List of matching companies with their information
    """
    try:
        # Use Yahoo Finance API to search for companies
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}&quotesCount={max_results}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'quotes' not in data:
            return []
            
        # Get information for each result
        companies = []
        for quote in data['quotes']:
            if quote.get('quoteType') != 'EQUITY':
                continue
                
            # Calculate similarity score
            similarity = fuzz.ratio(query.lower(), quote['longname'].lower())
            
            # Get additional info using yfinance
            try:
                ticker = yf.Ticker(quote['symbol'])
                info = ticker.info
                
                companies.append({
                    'name': quote['longname'],
                    'ticker': quote['symbol'],
                    'similarity': similarity,
                    'market': info.get('market', 'N/A'),
                    'exchange': info.get('exchange', 'N/A'),
                    'sector': info.get('sector', 'N/A'),
                    'industry': info.get('industry', 'N/A')
                })
            except:
                continue
        
        # Sort by similarity score and limit results
        companies.sort(key=lambda x: x['similarity'], reverse=True)
        return companies[:max_results]
        
    except Exception as e:
        print(f"Error searching for companies: {str(e)}")
        return []

def process_company_list(company_names: List[str]) -> List[Dict]:
    """
    Process a list of company names and find their ticker symbols.
    
    Args:
        company_names (List[str]): List of company names to search for
        
    Returns:
        List[Dict]: List of companies with their information
    """
    results = []
    for company_name in company_names:
        print(f"\nSearching for: {company_name}")
        matches = search_companies(company_name, max_results=1)
        
        if matches:
            # Get the best match
            best_match = matches[0]
            results.append({
                'input_name': company_name,
                'found_name': best_match['name'],
                'ticker': best_match['ticker'],
                'confidence': best_match['similarity'],
                'market': best_match['market'],
                'exchange': best_match['exchange'],
                'sector': best_match['sector'],
                'industry': best_match['industry']
            })
        else:
            results.append({
                'input_name': company_name,
                'found_name': 'Not Found',
                'ticker': 'N/A',
                'confidence': 0,
                'market': 'N/A',
                'exchange': 'N/A',
                'sector': 'N/A',
                'industry': 'N/A'
            })
    
    return results

def main():
    print("Choose an option:")
    print("1. Search for a single company")
    print("2. Process a list of companies")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\nEnter a company name (can be partial or misspelled)")
        print("Examples:")
        print("- 'appl' (will find Apple)")
        print("- 'microsoft' (will find Microsoft)")
        print("- 'amazon' (will find Amazon)")
        print("- 'google' (will find Google)")
        
        query = input("\nEnter company name: ").strip()
        
        if not query:
            print("Please enter a company name")
            return
            
        print("\nSearching for companies...")
        results = search_companies(query)
        
        if results:
            print("\nFound companies:")
            print("-" * 50)
            for company in results:
                print(f"\nName: {company['name']}")
                print(f"Ticker: {company['ticker']}")
                print(f"Match confidence: {company['similarity']}%")
                print(f"Market: {company['market']}")
                print(f"Exchange: {company['exchange']}")
                print(f"Sector: {company['sector']}")
                print(f"Industry: {company['industry']}")
                print("-" * 30)
        else:
            print("\nNo companies found. Try:")
            print("1. Using a different spelling")
            print("2. Using a partial name")
            print("3. Using common variations of the name")
            print("4. Checking if the company is publicly traded")
    
    elif choice == "2":
        print("\nEnter company names (one per line). Press Enter twice when done.")
        print("Example:")
        print("Apple Inc.")
        print("Microsoft Corporation")
        print("Amazon.com Inc.")
        print("[Press Enter]")
        print("[Press Enter]")
        
        companies = []
        while True:
            line = input().strip()
            if not line:
                break
            companies.append(line)
        
        if not companies:
            print("Please enter at least one company name")
            return
            
        print("\nProcessing company list...")
        results = process_company_list(companies)
        
        # Create a DataFrame for better display
        df = pd.DataFrame(results)
        print("\nResults:")
        print("-" * 100)
        print(df.to_string(index=False))
        
        # Save results to CSV
        output_file = "company_tickers.csv"
        df.to_csv(output_file, index=False)
        print(f"\nResults have been saved to {output_file}")
    
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main() 