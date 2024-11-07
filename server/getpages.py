# from pathlib import Path
# from PyPDF2 import PdfReader

# # Define the root directory
# root_dir = Path("./data/batches/batch_1")


# def calculate_total_pages(dir_path):
#     total_pages = 0
#     pdf_count = 0

#     for file in dir_path.rglob("*.pdf"):  # Only check PDF files
#         try:
#             # Open the PDF and count the pages
#             with open(file, "rb") as f:
#                 reader = PdfReader(f)
#                 num_pages = len(reader.pages)
#                 total_pages += num_pages
#                 pdf_count += 1
#                 print(f"File: {file} - Pages: {num_pages}")
#         except Exception as e:
#             print(f"Error reading PDF {file}: {e}")

#     print(f"\nTotal number of PDF files processed: {pdf_count}")
#     print(f"Total number of pages across all PDFs: {total_pages}")

# # Start the page counting process
# calculate_total_pages(root_dir)

from pathlib import Path
from PyPDF2 import PdfReader

# Define the root directory containing the batch folders
root_dir = Path("./data/batches")

# Define the page limit for each batch
page_limit = 2500

def calculate_pages_per_batch(root_dir):
    for batch_dir in root_dir.iterdir():
        # Only process directories that follow the batch naming convention
        if batch_dir.is_dir() and batch_dir.name.startswith("batch_"):
            total_pages = 0
            pdf_count = 0

            # Process each PDF in the current batch directory
            for file in batch_dir.rglob("*.pdf"):
                try:
                    with open(file, "rb") as f:
                        reader = PdfReader(f)
                        num_pages = len(reader.pages)
                        total_pages += num_pages
                        pdf_count += 1
                        #print(f"File: {file} - Pages: {num_pages}")
                except Exception as e:
                    print(f"Error reading PDF {file}: {e}")

            # Print results for the current batch
            print(f"\nBatch: {batch_dir.name}")
            print(f"Total PDF files processed: {pdf_count}")
            print(f"Total pages in {batch_dir.name}: {total_pages}")

            # Check if the batch exceeds the page limit
            if total_pages > page_limit:
                print(f"Warning: {batch_dir.name} exceeds {page_limit} pages!!!!!!!!!!!!!!\n")

# Start the page counting process for all batches
calculate_pages_per_batch(root_dir)
