from pathlib import Path
from PyPDF2 import PdfReader

# Define the root directory containing PDFs
root_dir = Path("./data/arpa-orders")
max_pages_allowed = 500
total_files = 10000  # Known total file count

def check_pdf_pages(file_path):
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            num_pages = len(reader.pages)

            # Print only if the PDF exceeds the maximum page count
            if num_pages > max_pages_allowed:
                print(f"{file_path.name}: OVER LIMIT - {num_pages} pages")

    except Exception as e:
        # Print an error message if the file cannot be read
        print(f"{file_path.name}: ERROR - {e}")

def process_pdfs(dir_path):
    pdf_files = list(dir_path.rglob("*.pdf"))  # Find all PDFs in directory
    processed_files = 0
    total_to_check = len(pdf_files)

    print(f"Checking {total_to_check} PDF files...")

    for file in pdf_files:
        check_pdf_pages(file)
        processed_files += 1

        # Print progress in the format "Processed X of 10000 files"
        if processed_files % 100 == 0 or processed_files == total_to_check:
            print(f"Progress: Processed {processed_files} of {total_files} files")

# Start processing PDFs
process_pdfs(root_dir)
