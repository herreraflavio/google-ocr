from pathlib import Path

# root_dir = Path("./data/arpa-orders-sample")
root_dir = Path("./data/arpa-orders-sample")
total_files = 0

def find_pdf_files(dir_path):
    global total_files
    for pdf_file in dir_path.rglob("*.pdf"):  # Recursively find .pdf files
        total_files += 1
        # print(f"PDF File: {pdf_file.name} (Path: {pdf_file})")

# Start the search
find_pdf_files(root_dir)
print(f"Total PDF files found: {total_files}")