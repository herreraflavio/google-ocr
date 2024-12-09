import os
import json
import fitz  # PyMuPDF

def extract_text_from_pdfs(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(input_dir, file_name)
            output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")
            
            try:
                # Open and extract text from the PDF
                doc = fitz.open(pdf_path)
                text = ""
                for page in doc:
                    text += page.get_text()  # Extracts text using layout-aware OCR
                doc.close()
                
                # Save text to JSON
                data = {"text": text}
                with open(output_file, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, indent=4)
                
                print(f"Processed: {file_name}")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

# Directories
input_directory = "outputpdfs"
output_directory = "outputjson_fitz"

# Extract text and save as JSON
extract_text_from_pdfs(input_directory, output_directory)
