import os
from pdftocsv import process_pdfs
from filterer import parse_invoice_text
from database.db_handler import DatabaseHandler

def main():
    # Get base directory and setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdfs_folder = os.path.join(base_dir, 'pdfs')

    # Initialize database
    db_handler = DatabaseHandler()

    # Process PDFs and store in database
    raw_texts = process_pdfs(pdfs_folder)
    
    for pdf_filename, text in raw_texts.items():
        parsed_data = parse_invoice_text(text)
        db_handler.insert_records(parsed_data)

if __name__ == "__main__":
    main()
