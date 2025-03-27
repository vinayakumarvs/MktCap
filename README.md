# Company Information and Ticker Symbol Finder

This repository contains two Python scripts for finding company information and ticker symbols using the Yahoo Finance API.

## Scripts Overview

### 1. company_info.py
This script allows you to get detailed information about a company using its ticker symbol.

### 2. search_ticker.py
This script helps you find company ticker symbols and information using company names, even with partial or misspelled names.

## Features

- Search for companies by name or ticker symbol
- Get detailed company information including:
  - Company name
  - Ticker symbol
  - Market
  - Exchange
  - Market cap
  - Sector
  - Industry
- Process multiple companies at once
- Export results to CSV
- Fuzzy matching for company names
- Confidence scores for matches

## Requirements

Install the required packages using pip:
```bash
pip install -r requirements.txt
```

Required packages:
- yfinance >= 0.2.36
- pandas >= 2.0.0
- fuzzywuzzy >= 0.18.0
- python-Levenshtein >= 0.21.0
- requests >= 2.31.0

## Usage

### Using company_info.py

This script is used to get detailed information about a company using its ticker symbol.

```bash
python company_info.py
```

Example:
```
Enter the stock ticker symbol (e.g., 'AAPL' for Apple, 'MSFT' for Microsoft)
Ticker symbol: AAPL
```

### Using search_ticker.py

This script offers two modes:

1. Single Company Search:
```bash
python search_ticker.py
```
Then choose option 1 and enter a company name.

2. Multiple Companies Search:
```bash
python search_ticker.py
```
Then choose option 2 and enter multiple company names, one per line.

Example input for multiple companies:
```
Apple Inc.
Microsoft Corporation
Amazon.com Inc.
[Press Enter]
[Press Enter]
```

The results will be:
- Displayed in the terminal
- Saved to `company_tickers.csv`

## Output Format

### Single Company Search
```
Company Information:
--------------------------------------------------
Name: Apple Inc.
Ticker Symbol: AAPL
Market: US
Exchange: NMS
Market Cap: 2,500,000,000,000 USD
Sector: Technology
Industry: Consumer Electronics
--------------------------------------------------
```

### Multiple Companies Search (CSV Format)
The output CSV file contains the following columns:
- input_name: The name you entered
- found_name: The official company name
- ticker: The company's ticker symbol
- confidence: Match confidence percentage
- market: The market where the stock is traded
- exchange: The stock exchange
- sector: Company's sector
- industry: Company's industry

## Tips for Better Results

1. For company_info.py:
   - Use the correct ticker symbol
   - Check if the company is publicly traded
   - Use the correct exchange suffix if needed (e.g., '.L' for London)

2. For search_ticker.py:
   - Use the company's common name
   - Try different variations of the name
   - Use partial names if you're unsure
   - Check the confidence score to verify matches

## Common Ticker Examples

- AAPL: Apple Inc.
- MSFT: Microsoft Corporation
- GOOGL: Google (Alphabet)
- AMZN: Amazon.com Inc.
- META: Meta Platforms (Facebook)
- TSLA: Tesla Inc.
- NVDA: NVIDIA Corporation
- JPM: JPMorgan Chase & Co.
- V: Visa Inc.
- WMT: Walmart Inc.

## Error Handling

Both scripts include error handling for:
- Invalid ticker symbols
- Network issues
- API rate limits
- Missing company information

## Note

The scripts use the Yahoo Finance API, which may have rate limits or occasional downtime. If you encounter issues, please wait a few minutes and try again. 