# from pathlib import Path
# from PyPDF2 import PdfReader, PdfWriter

# root_dir = Path("./data/arpa-orders")
# needs_repair_dir = Path("./data/needs_repair")
# partially_corrupted_dir = Path("./data/partially_corrupted")

# total_files = 0
# max_pages_per_pdf = 499  # Maximum pages allowed per split PDF

# def split_pdf(file, num_pages):
#     base_name = file.stem
#     output_dir = file.parent

#     # Calculate the number of sections
#     num_sections = (num_pages // max_pages_per_pdf) + (1 if num_pages % max_pages_per_pdf != 0 else 0)

#     with open(file, "rb") as f:
#         reader = PdfReader(f)

#         for section in range(num_sections):
#             start_page = section * max_pages_per_pdf
#             end_page = min(start_page + max_pages_per_pdf, num_pages)

#             writer = PdfWriter()
#             for page_num in range(start_page, end_page):
#                 writer.add_page(reader.pages[page_num])

#             # Define new file name with section suffix
#             section_file_name = f"{base_name}_section{section + 1}.pdf"
#             section_file_path = output_dir / section_file_name

#             # Write the new PDF section
#             with open(section_file_path, "wb") as output_pdf:
#                 writer.write(output_pdf)

#             print(f"Created: {section_file_name} (Pages: {end_page - start_page})")

# def find_files(dir_path):
#     global total_files
#     for file in dir_path.rglob("*.pdf"):  # Filter only for PDFs
#         total_files += 1

#         try:
#             # First open the file and get page count
#             with open(file, "rb") as f:
#                 reader = PdfReader(f)
#                 num_pages = len(reader.pages)

#             # If file has more than the allowed pages, split it
#             if num_pages > max_pages_per_pdf:
#                 print(f"Splitting PDF File: {file.name} (Total Pages: {num_pages}, Path: {file})")
#                 split_pdf(file, num_pages)
                
#                 # Close file and delete after splitting
#                 file.unlink()
#                 print(f"Deleted original file: {file.name}")
#             # else:
#             #     print(f"PDF File: {file.name} (Pages: {num_pages}, Path: {file})")

#         except Exception as e:
#             print(f"Error reading PDF {file.name}: {e}")

# # Start the search
# find_files(root_dir)
# print(f"Total PDF files processed: {total_files}")

from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
import shutil

root_dir = Path("./data/arpa-orders")
needs_repair_dir = Path("./data/needs_repair")
partially_corrupted_dir = Path("./data/partially_corrupted")

# Ensure directories exist
needs_repair_dir.mkdir(parents=True, exist_ok=True)
partially_corrupted_dir.mkdir(parents=True, exist_ok=True)

total_files = 0
max_pages_per_pdf = 499  # Maximum pages allowed per split PDF

def split_pdf(file, num_pages):
    base_name = file.stem
    output_dir = file.parent

    # Calculate the number of sections
    num_sections = (num_pages // max_pages_per_pdf) + (1 if num_pages % max_pages_per_pdf != 0 else 0)

    with open(file, "rb") as f:
        reader = PdfReader(f)

        for section in range(num_sections):
            start_page = section * max_pages_per_pdf
            end_page = min(start_page + max_pages_per_pdf, num_pages)

            writer = PdfWriter()
            for page_num in range(start_page, end_page):
                try:
                    writer.add_page(reader.pages[page_num])
                except Exception as e:
                    print(f"Error adding page {page_num} in {file.name}: {e}")
                    # Move to partially corrupted directory if page error occurs
                    shutil.move(file, partially_corrupted_dir / file.name)
                    return  # Stop further processing for this file

            # Define new file name with section suffix
            section_file_name = f"{base_name}_section{section + 1}.pdf"
            section_file_path = output_dir / section_file_name

            # Write the new PDF section
            with open(section_file_path, "wb") as output_pdf:
                writer.write(output_pdf)

            print(f"Created: {section_file_name} (Pages: {end_page - start_page})")

def find_files(dir_path):
    global total_files
    for file in dir_path.rglob("*.pdf"):  # Filter only for PDFs
        total_files += 1

        try:
            # First open the file and get page count
            with open(file, "rb") as f:
                reader = PdfReader(f)
                num_pages = len(reader.pages)

            # If file has more than the allowed pages, split it
            if num_pages > max_pages_per_pdf:
                print(f"Splitting PDF File: {file.name} (Total Pages: {num_pages}, Path: {file})")
                split_pdf(file, num_pages)
                
                # Close file and delete after splitting
                file.unlink()
                print(f"Deleted original file: {file.name}")

        except Exception as e:
            print(f"Error reading PDF {file.name}: {e}")
            error_message = str(e).lower()

            # Move file based on error type
            if "xref" in error_message or "startxref" in error_message:
                shutil.move(file, needs_repair_dir / file.name)
                print(f"Moved {file.name} to needs_repair directory due to cross-reference error.")
            else:
                shutil.move(file, partially_corrupted_dir / file.name)
                print(f"Moved {file.name} to partially_corrupted directory due to severe corruption.")

# Start the search
find_files(root_dir)
print(f"Total PDF files processed: {total_files}")
