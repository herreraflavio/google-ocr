# from pathlib import Path
# from PyPDF2 import PdfReader
# from concurrent.futures import ThreadPoolExecutor, as_completed

# # Define the root directory
# root_dir = Path("./data/arpa-orders")

# # Function to check if a PDF is corrupt
# def check_pdf(file):
#     try:
#         # Try to open the PDF and read pages
#         with open(file, "rb") as f:
#             reader = PdfReader(f)
#             # Attempt to access the first page
#             _ = reader.pages[0]  # Trigger an error if the PDF is corrupt
#         return {"file_name": file.name, "file_path": str(file), "is_corrupt": False}
#     except Exception as e:
#         return {"file_name": file.name, "file_path": str(file), "is_corrupt": True, "error": str(e)}

# def check_corrupt_pdfs(dir_path, max_workers=4):
#     pdf_files = list(dir_path.rglob("*.pdf"))  # Only check PDF files
#     total_files = len(pdf_files)
#     corrupt_files = []

#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = {executor.submit(check_pdf, file): file for file in pdf_files}
        
#         for future in as_completed(futures):
#             result = future.result()
#             if result["is_corrupt"]:
#                 corrupt_files.append(result)
#                 print(f"Corrupt PDF detected: {result['file_path']} - {result['error']}")
#             else:
#                 print(f"Checked: {result['file_path']} - OK")

#     # Summary of results
#     corrupt_count = len(corrupt_files)
#     print(f"\nTotal PDF files checked: {total_files}")
#     print(f"Total corrupt PDF files: {corrupt_count}")

#     if corrupt_files:
#         print("\nList of corrupt PDF files:")
#         for entry in corrupt_files:
#             print(f"File: {entry['file_name']}, Path: {entry['file_path']}, Error: {entry['error']}")
#     else:
#         print("No corrupt PDF files found.")

# # Start checking for corrupt PDFs with parallel processing
# check_corrupt_pdfs(root_dir, max_workers=8)

# from pathlib import Path
# from PyPDF2 import PdfReader
# from concurrent.futures import ThreadPoolExecutor, as_completed

# # Define the root directory
# root_dir = Path("./data/arpa-orders")

# # Function to check if a PDF is corrupt
# def check_pdf(file):
#     try:
#         # Try to open the PDF and read pages
#         with open(file, "rb") as f:
#             reader = PdfReader(f)
#             # Attempt to access the first page
#             _ = reader.pages[0]  # Trigger an error if the PDF is corrupt
#         return {"file_name": file.name, "file_path": str(file), "is_corrupt": False}
#     except Exception as e:
#         return {"file_name": file.name, "file_path": str(file), "is_corrupt": True, "error": str(e)}

# def check_corrupt_pdfs(dir_path, max_workers=8):
#     pdf_files = list(dir_path.rglob("*.pdf"))  # Only check PDF files
#     total_files = len(pdf_files)
#     corrupt_files = []

#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = {executor.submit(check_pdf, file): file for file in pdf_files}
        
#         for future in as_completed(futures):
#             result = future.result()
#             if result["is_corrupt"]:
#                 corrupt_files.append(result)
#                 print(f"Corrupt PDF detected: {result['file_path']} - {result['error']}")
#             else:
#                 print(f"Checked: {result['file_path']} - OK")

#     # Summary of results
#     corrupt_count = len(corrupt_files)
#     corrupt_ratio = (corrupt_count / total_files) * 100 if total_files > 0 else 0
#     print(f"\nTotal PDF files checked: {total_files}")
#     print(f"Total corrupt PDF files: {corrupt_count}")
#     print(f"Corrupt PDF percentage: {corrupt_ratio:.2f}%")

#     if corrupt_files:
#         print("\nList of corrupt PDF files:")
#         for entry in corrupt_files:
#             print(f"File: {entry['file_name']}, Path: {entry['file_path']}, Error: {entry['error']}")
#     else:
#         print("No corrupt PDF files found.")

# # Start checking for corrupt PDFs with parallel processing
# check_corrupt_pdfs(root_dir, max_workers=8)

# from pathlib import Path
# from PyPDF2 import PdfReader
# from concurrent.futures import ThreadPoolExecutor, as_completed

# # Define the root directory and the total number of files
# root_dir = Path("./data/arpa-orders")
# corrupted_dir = Path("./data/corrupted")
# total_files = 14000  # Known total file count

# # Function to check if a PDF is corrupt
# def check_pdf(file):
#     try:
#         # Try to open the PDF and read pages
#         with open(file, "rb") as f:
#             reader = PdfReader(f)
#             # Attempt to access the first page
#             _ = reader.pages[0]  # Trigger an error if the PDF is corrupt
#         return {"file_name": file.name, "file_path": str(file), "is_corrupt": False}
#     except Exception as e:
#         return {"file_name": file.name, "file_path": str(file), "is_corrupt": True, "error": str(e)}

# def check_corrupt_pdfs(dir_path, max_workers=8):
#     pdf_files = list(dir_path.rglob("*.pdf"))  # Only check PDF files
#     corrupt_count = 0
#     checked_files = 0

#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = {executor.submit(check_pdf, file): file for file in pdf_files}
        
#         for future in as_completed(futures):
#             result = future.result()
#             checked_files += 1

#             if result["is_corrupt"]:
#                 corrupt_count += 1
#                 print(f"Corrupt PDF detected: {result['file_path']} - {result['error']}")
#             else:
#                 print(f"Checked: {result['file_path']} - OK")

#             # Calculate and display progress
#             corrupt_ratio = (corrupt_count / checked_files) * 100
#             completion_ratio = (checked_files / total_files) * 100
#             print(f"Progress: {checked_files}/{total_files} files checked ({completion_ratio:.2f}%), Corrupt PDFs: {corrupt_count} ({corrupt_ratio:.2f}%)")

#     # Final summary
#     print(f"\nTotal PDF files checked: {checked_files}")
#     print(f"Total corrupt PDF files: {corrupt_count}")
#     final_corrupt_ratio = (corrupt_count / checked_files) * 100 if checked_files > 0 else 0
#     print(f"Final Corrupt PDF percentage: {final_corrupt_ratio:.2f}%")

# # Start checking for corrupt PDFs with parallel processing
# check_corrupt_pdfs(root_dir, max_workers=8)

from pathlib import Path
from PyPDF2 import PdfReader
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil

# Define the root directory and the corrupted files directory
root_dir = Path("./data/arpa-orders")
corrupted_dir = Path("./data/corrupted")
total_files = 10105  # Known total file count

# Ensure corrupted directory exists
corrupted_dir.mkdir(parents=True, exist_ok=True)

# Function to check if a PDF is corrupt and move it if necessary
def check_pdf(file):
    try:
        # Try to open the PDF and read pages
        with open(file, "rb") as f:
            reader = PdfReader(f)
            # Attempt to access the first page
            _ = reader.pages[0]  # Trigger an error if the PDF is corrupt
        return {"file_name": file.name, "file_path": str(file), "is_corrupt": False}
    except Exception as e:
        # Move the corrupt file to the corrupted directory
        corrupted_path = corrupted_dir / file.name
        shutil.move(file, corrupted_path)
        return {"file_name": file.name, "file_path": str(corrupted_path), "is_corrupt": True, "error": str(e)}

def check_corrupt_pdfs(dir_path, max_workers=8):
    pdf_files = list(dir_path.rglob("*.pdf"))  # Only check PDF files
    corrupt_count = 0
    checked_files = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_pdf, file): file for file in pdf_files}
        
        for future in as_completed(futures):
            result = future.result()
            checked_files += 1

            if result["is_corrupt"]:
                corrupt_count += 1
                print(f"Corrupt PDF detected and moved: {result['file_path']} - {result['error']}")
            else:
                print(f"Checked: {result['file_path']} - OK")

            # Calculate and display progress
            corrupt_ratio = (corrupt_count / checked_files) * 100
            completion_ratio = (checked_files / total_files) * 100
            print(f"Progress: {checked_files}/{total_files} files checked ({completion_ratio:.2f}%), Corrupt PDFs: {corrupt_count} ({corrupt_ratio:.2f}%)")

    # Final summary
    print(f"\nTotal PDF files checked: {checked_files}")
    print(f"Total corrupt PDF files: {corrupt_count}")
    final_corrupt_ratio = (corrupt_count / checked_files) * 100 if checked_files > 0 else 0
    print(f"Final Corrupt PDF percentage: {final_corrupt_ratio:.2f}%")

# Start checking for corrupt PDFs with parallel processing
check_corrupt_pdfs(root_dir, max_workers=8)
