import os
import PyPDF2

def convert_pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        return text

def process_pdfs(pdfs_folder):
    results = {}
    for pdf_filename in os.listdir(pdfs_folder):
        if pdf_filename.endswith('.pdf'):
            pdf_path = os.path.join(pdfs_folder, pdf_filename)
            results[pdf_filename] = convert_pdf_to_text(pdf_path)
    return results
