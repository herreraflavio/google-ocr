import os
from PyPDF2 import PdfReader

# Function to extract text from each page of the PDF and save it in separate text files
def extract_text_from_pdf(pdf_path, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        total_pages = len(reader.pages)
        
        # Loop through each page and extract text
        for page_num in range(total_pages):
            page = reader.pages[page_num]
            page_text = page.extract_text()

            # Create a text file for each page
            output_file = os.path.join(output_dir, f'page_{page_num + 1}.txt')
            with open(output_file, 'w', encoding='utf-8') as txt_file:
                txt_file.write(page_text if page_text else "No text found on this page.")
            
            print(f'Text from page {page_num + 1} has been saved to {output_file}.')

# Usage example
pdf_path = 'pg101.pdf'  # Replace with your PDF file path
output_dir = 'txt_files'  # Directory to store the text files
extract_text_from_pdf(pdf_path, output_dir)
