# filepath: /path/to/your/file.py

import os
import PyPDF2
import re

def convert_pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text
        return text

def process_pdfs(pdfs_folder):
    results = {}
    for pdf_filename in os.listdir(pdfs_folder):
        if pdf_filename.endswith('.pdf'):
            pdf_path = os.path.join(pdfs_folder, pdf_filename)
            text = convert_pdf_to_text(pdf_path)
            # Extract first and last names from text
            first_name = extract_first_name(text)
            last_name = extract_last_name(text)
            results[pdf_filename] = {
                'text': text,
                'first_name': first_name,
                'last_name': last_name
            }
    return results

def extract_first_name(text):
    """Extract the first name from the PDF text."""
    match = re.search(r'Passenger name:\s+(?:Mr\.|Ms\.)\s+([A-Z]+)', text)
    return match.group(1) if match else ''

def extract_last_name(text):
    """Extract the last name from the PDF text."""
    match = re.search(r'Passenger name:\s+(?:Mr\.|Ms\.)\s+[A-Z]+\s+([A-Z]+)', text)
    return match.group(1) if match else ''
