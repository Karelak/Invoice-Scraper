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
│   ├── database/    # Database handling
│   ├── filterer.py  # Invoice parsing logic
│   ├── main.py      # Main execution script
│   └── pdftocsv.py  # PDF processing
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

1. Place airBaltic PDF invoices in the `pdfs/` directory
2. Run the script:
   ```bash
   python -m src.main
   ```
3. Results will be stored in `invoices.db`

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
