import os
import argparse
from src.converter.pdftocsv import process_pdfs
from src.converter.filterer import parse_invoice_text
from src.database.db_handler import DatabaseHandler

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Invoice Scraper")
    parser.add_argument('pdfs_folder', type=str, help="Path to the folder containing PDF invoices")
    parser.add_argument('db_path', type=str, help="Path to the SQLite database file")
    args = parser.parse_args()

    pdfs_folder = args.pdfs_folder
    db_path = args.db_path

    # Initialize database
    db_handler = DatabaseHandler(db_path)

    # Process PDFs and store in database
    print(f"Processing PDFs in folder: {pdfs_folder}")
    raw_texts = process_pdfs(pdfs_folder)
    
    for pdf_filename, text in raw_texts.items():
        print(f"Parsing invoice: {pdf_filename}")
        parsed_data = parse_invoice_text(text)
        db_handler.insert_records(parsed_data)
        print(f"Inserted data for: {pdf_filename}")

    print(f"All invoices processed. Data stored in: {db_path}")

if __name__ == "__main__":
    main()
