# from pathlib import Path

# root_dir = Path("./data/arpa-orders-sample")
# total_files = 0

# def find_files(dir_path):
#     global total_files
#     for file in dir_path.rglob("*"):  # Recursively find all files
#         if file.suffix in {".pdf", ".txt"}:  # Check for .pdf or .txt extensions
#             total_files += 1
#             print(f"File: {file.name} (Path: {file})")

# # Start the search
# find_files(root_dir)
# print(f"Total PDF and TXT files found: {total_files}")


# prints out files that have more than 500 pages
# from pathlib import Path
# from PyPDF2 import PdfReader

# root_dir = Path("./data/arpa-orders-sample")
# total_files = 0

# def find_files(dir_path):
#     global total_files
#     for file in dir_path.rglob("*"):
#         if file.suffix in {".pdf", ".txt"}:
#             total_files += 1

#             if file.suffix == ".pdf":
#                 try:
#                     with open(file, "rb") as f:
#                         reader = PdfReader(f)
#                         num_pages = len(reader.pages)
#                         if num_pages >= 500:
#                             print(f"PDF File: {file.name} (Pages: {num_pages}, Path: {file})")
                            
#                 except Exception as e:
#                     print(f"Error reading PDF {file.name}: {e}")

# # Start the search
# find_files(root_dir)
# print(f"Total PDF and TXT files found: {total_files}")

# working code
# from pathlib import Path
# from PyPDF2 import PdfReader

# root_dir = Path("./data/arpa-orders-sample")
# virtual_batches = []  # Initialize an empty list of virtual batches
# max_batch_size_mb = 1000
# max_batch_pages = 2500

# def find_files(dir_path):
#     current_batch = {"paths": [], "total_size_mb": 0, "total_pages": 0}

#     for file in dir_path.rglob("*.pdf"):
#         file_size_mb = file.stat().st_size / (1024 * 1024)  # Convert bytes to MB
        
#         try:
#             with open(file, "rb") as f:
#                 reader = PdfReader(f)
#                 num_pages = len(reader.pages)
                
#                 # Skip files with more than 500 pages
#                 if num_pages > 500:
#                     continue

#                 # Check if the file fits in the current batch, otherwise create a new batch
#                 if (current_batch["total_size_mb"] + file_size_mb > max_batch_size_mb or 
#                     current_batch["total_pages"] + num_pages > max_batch_pages):
                    
#                     # Finalize the current batch and start a new one
#                     virtual_batches.append(current_batch)
#                     current_batch = {"paths": [], "total_size_mb": 0, "total_pages": 0}

#                 # Add file to the current batch
#                 current_batch["paths"].append(str(file))
#                 current_batch["total_size_mb"] += file_size_mb
#                 current_batch["total_pages"] += num_pages

#         except Exception as e:
#             print(f"Error reading PDF {file.name}: {e}")
    
#     # Append the last batch if it has any files
#     if current_batch["paths"]:
#         virtual_batches.append(current_batch)

# # Start the search
# find_files(root_dir)

# # Output virtual batches
# for i, batch in enumerate(virtual_batches, start=1):
#     print(f"Batch {i}:")
#     print(f"  Total Size (MB): {batch['total_size_mb']:.2f}")
#     print(f"  Total Pages: {batch['total_pages']}")
#     print(f"  File Paths: {batch['paths']}")
# print(f"\nTotal Batches Created: {len(virtual_batches)}")

#move files
from pathlib import Path
from PyPDF2 import PdfReader
import shutil

# Define the root directory for the source files and the target batches directory
root_dir = Path("./data/arpa-orders")
batches_dir = Path("./data/batches")
batches_dir.mkdir(exist_ok=True)  # Ensure the batches directory exists

virtual_batches = []  # Initialize an empty list of virtual batches
max_batch_size_mb = 1000
max_batch_pages = 2500

def find_files(dir_path):
    current_batch = {"paths": [], "total_size_mb": 0, "total_pages": 0}
    batch_count = 1

    for file in dir_path.rglob("*.pdf"):
        file_size_mb = file.stat().st_size / (1024 * 1024)  # Convert bytes to MB
        
        try:
            with open(file, "rb") as f:
                reader = PdfReader(f)
                num_pages = len(reader.pages)
                
                # Skip files with more than 500 pages
                if num_pages > 500:
                    continue

                # Check if the file fits in the current batch, otherwise create a new batch folder and move files
                if (current_batch["total_size_mb"] + file_size_mb > max_batch_size_mb or 
                    current_batch["total_pages"] + num_pages > max_batch_pages):
                    
                    # Create a new directory for the batch
                    batch_dir = batches_dir / f"batch_{batch_count}"
                    batch_dir.mkdir(exist_ok=True)
                    
                    # Move files to the new batch directory
                    for file_path in current_batch["paths"]:
                        shutil.move(file_path, batch_dir / Path(file_path).name)

                    # Finalize the current batch and start a new one
                    virtual_batches.append(current_batch)
                    current_batch = {"paths": [], "total_size_mb": 0, "total_pages": 0}
                    batch_count += 1

                # Add file to the current batch
                current_batch["paths"].append(str(file))
                current_batch["total_size_mb"] += file_size_mb
                current_batch["total_pages"] += num_pages

        except Exception as e:
            print(f"Error reading PDF {file.name}: {e}")
    
    # Move files of the last batch if it has any files
    if current_batch["paths"]:
        batch_dir = batches_dir / f"batch_{batch_count}"
        batch_dir.mkdir(exist_ok=True)
        for file_path in current_batch["paths"]:
            shutil.move(file_path, batch_dir / Path(file_path).name)
        virtual_batches.append(current_batch)

# Start the search
find_files(root_dir)

# Output virtual batches
for i, batch in enumerate(virtual_batches, start=1):
    print(f"Batch {i}:")
    print(f"  Total Size (MB): {batch['total_size_mb']:.2f}")
    print(f"  Total Pages: {batch['total_pages']}")
    print(f"  File Paths: {batch['paths']}")
print(f"\nTotal Batches Created: {len(virtual_batches)}")
