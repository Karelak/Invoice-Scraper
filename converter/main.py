import os
from raw_converter import process_pdfs
from filterer import parse_invoice_text, save_to_csv

def main():
    # Get base directory and setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdfs_folder = os.path.join(base_dir, 'pdfs')
    csvs_folder = os.path.join(base_dir, 'csvs')

    # Create csvs folder if it doesn't exist
    if not os.path.exists(csvs_folder):
        os.makedirs(csvs_folder)

    # Step 1: Convert PDFs to text
    raw_texts = process_pdfs(pdfs_folder)

    # Step 2: Parse and save each invoice
    for pdf_filename, text in raw_texts.items():
        # Parse the text
        parsed_data = parse_invoice_text(text)
        
        # Create CSV filename
        csv_filename = pdf_filename.replace('.pdf', '.csv')
        csv_path = os.path.join(csvs_folder, csv_filename)
        
        # Save to CSV
        save_to_csv(parsed_data, csv_path)

if __name__ == "__main__":
    main()
