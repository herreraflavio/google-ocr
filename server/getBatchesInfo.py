import os
import json

# Specify the path to the JSON file and the base directory for batches
json_file_path = 'unique_folders.json'
directory_path = './data/batches'

# Load the JSON array of folder names
with open(json_file_path, 'r') as f:
    folder_list = json.load(f)

# Initialize counters for the total size and the total number of PDF files
total_size = 0  # Total size in bytes
total_pdf_count = 0  # Total PDF files count

# Traverse each folder in the JSON array
for folder_name in folder_list:
    folder_path = os.path.join(directory_path, folder_name)
    
    # Check if the folder exists
    if os.path.isdir(folder_path):
        # Traverse all files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            # Check if it's a file (ignore subdirectories)
            if os.path.isfile(file_path):
                # Add the file size to the total size
                total_size += os.path.getsize(file_path)
                
                # Check if the file is a PDF
                if file_name.lower().endswith('.pdf'):
                    total_pdf_count += 1

# Convert total size to GB
total_size_gb = round(total_size / (1024 * 1024 * 1024), 2)

# Print the results
print(f"Total size of files in specified folders: {total_size_gb} GB")
print(f"Total number of PDF files in specified folders: {total_pdf_count}")
