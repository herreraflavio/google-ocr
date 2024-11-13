import fitz  # PyMuPDF
import os
from google.cloud import storage

def get_local_pdf_page_counts(folder_path):
    """
    Retrieves the page count of each PDF file in a local folder.
    """
    pdf_page_counts = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            try:
                # Open PDF and get page count
                with fitz.open(file_path) as pdf:
                    page_count = pdf.page_count
                pdf_page_counts[filename] = page_count
                print(f"{filename}: {page_count} pages")
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return pdf_page_counts

def split_by_page_count(pdf_page_counts):
    """
    Splits PDFs into two groups with approximately equal total page counts.
    """
    # Sort PDFs by page count in descending order
    pdf_page_counts_sorted = sorted(pdf_page_counts.items(), key=lambda x: x[1], reverse=True)

    group1 = []
    group2 = []
    total1, total2 = 0, 0

    # Greedily assign each PDF to the group with the smaller total page count
    for filename, page_count in pdf_page_counts_sorted:
        if total1 <= total2:
            group1.append(filename)
            total1 += page_count
        else:
            group2.append(filename)
            total2 += page_count

    print(f"Total pages in Group 1 (original folder): {total1}")
    print(f"Total pages in Group 2 (batch_739): {total2}")
    return group1, group2

def move_gcs_files(bucket_name, source_folder, destination_folder, files_to_move):
    """
    Moves files in the Google Cloud Storage bucket to a new folder.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for file_name in files_to_move:
        source_blob = bucket.blob(f"{source_folder}/{file_name}")
        destination_blob_name = f"{destination_folder}/{file_name}"
        
        # Copy the file to the new location
        bucket.copy_blob(source_blob, bucket, destination_blob_name)
        # Delete the original file after copying
        source_blob.delete()

        print(f"Moved {file_name} to {destination_blob_name}")

def main():
    # Replace these variables with your actual information
    bucket_name = "testbucketarpa"
    local_batch_folder = "./data/batches/batch_5"  # Path to the local batch folder
    source_folder = "arpa-orders/batch_5"  # Folder in GCS where the PDFs are
    new_batch_folder = "arpa-orders/batch_743"  # New folder name for the moved files

    # Step 1: Get page counts for each PDF in the local batch
    local_page_counts = get_local_pdf_page_counts(local_batch_folder)

    # Step 2: Split the PDFs into two groups based on local page counts
    # Group1 will stay in the original GCS folder, and Group2 will be moved to batch_739
    group1_files, group2_files = split_by_page_count(local_page_counts)

    # Step 3: Move Group2 files from the original GCS folder to the batch_739 folder
    move_gcs_files(bucket_name, source_folder, new_batch_folder, group2_files)

if __name__ == "__main__":
    main()
