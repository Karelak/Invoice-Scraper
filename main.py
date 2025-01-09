import os
import argparse
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from threading import Thread
from src.converter.pdftocsv import process_pdfs
from src.converter.filterer import parse_invoice_text
from src.database.db_handler import DatabaseHandler

def process_invoice(pdf_filename, data, queue):
    text = data['text']
    parsed_data = parse_invoice_text(text)
    # Update with name data extracted from process_pdfs
    if 'first_name' in data and data['first_name']:
        parsed_data['first_name'] = data['first_name']
    if 'last_name' in data and data['last_name']:
        parsed_data['last_name'] = data['last_name']
    queue.put(parsed_data)

def db_writer(queue, db_handler):
    while True:
        records = queue.get()
        if records is None:
            break
        db_handler.insert_records(records)
        queue.task_done()

def clean_path(path):
    """Clean and validate a file system path."""
    # Remove common problematic characters and clean the path
    path = path.strip()
    
    # Handle the case where path starts with & and contains quotes
    if path.startswith('&'):
        path = path.lstrip('&').strip()
    
    # Remove any remaining quotes
    path = path.strip("'").strip('"')
    
    # Remove any duplicate backslashes and normalize path
    path = os.path.normpath(path)
    
    return path

def validate_paths(pdfs_folder, db_path):
    """Validate the provided paths."""
    # Validate PDF folder
    if not os.path.exists(pdfs_folder):
        raise ValueError(f"PDF folder does not exist: {pdfs_folder}")
    
    # Ensure db directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        raise ValueError(f"Database directory does not exist: {db_dir}")

def main():
    # Get paths from user input and clean them
    print("Please enter paths without quotes or special characters")
    pdfs_folder = clean_path(input("Enter the path to the folder containing PDF invoices: "))
    db_path = clean_path(input("Enter the path for the SQLite database file: "))

    # Validate paths before proceeding
    try:
        validate_paths(pdfs_folder, db_path)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Initialize database
    db_handler = DatabaseHandler(db_path)

    # Process PDFs and store in database
    print(f"Processing PDFs in folder: {pdfs_folder}")
    raw_texts = process_pdfs(pdfs_folder)

    queue = Queue()
    writer_thread = Thread(target=db_writer, args=(queue, db_handler))
    writer_thread.start()

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_invoice, pdf_filename, data, queue) for pdf_filename, data in raw_texts.items()]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing PDFs"):
            future.result()

    queue.put(None)
    writer_thread.join()

    print(f"All invoices processed. Data stored in: {db_path}")

if __name__ == "__main__":
    main()
