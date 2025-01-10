# Invoice Scraper

Automated tool for extracting data from PDF invoices and storing it in a SQLite database. Specifically designed to parse airBaltic invoice PDFs and extract structured data including flight details, passenger information, and pricing.

## Features

- PDF text extraction
- Structured data parsing for airBaltic invoices
- SQLite database storage
- Support for multi-flight bookings
- Passenger information extraction
- Price breakdown storage

## Structure

```
├── pdfs/            # Input PDF files
├── src/             # Source code
│   ├── converter/   # PDF processing and invoice parsing
│   │   ├── pdftocsv.py
│   │   └── filterer.py
│   ├── database/    # Database handling
│   │   └── db_handler.py
│   └── __init__.py
├── main.py          # Main execution script
└── invoices.db      # SQLite database
```

## Requirements

- Python 3.8 or higher
- PyPDF2 3.0.0 or higher

## Setup

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix: `source venv/bin/activate`
4. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place airBaltic PDF invoices in a folder
2. Run the script:

   ```bash
   python main.py
   ```

3. Results will be stored in the specified SQLite database file

## Database Schema

The SQLite database contains a single table `invoices` with the following columns:

- Invoice Number
- Booking Reference
- Booking Date
- First Name
- Last Name
- Date
- Departure Time
- Arrival Time
- Route
- Fare
- Taxes
- Fuel Surcharge
- Ticketing Service
- Total
