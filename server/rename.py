# from pathlib import Path

# # Define the root directory
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

# from pathlib import Path

# # Define the root directory
# root_dir = Path("./data/arpa-orders-sample")
# total_files = 0

# def find_and_rename_files(dir_path):
#     global total_files
#     for file in dir_path.rglob("*.pdf"):  # Recursively find .pdf files
#         # Extract relevant parts of the path
#         parts = file.relative_to(root_dir).parts
        
#         # Check that there are enough parts to match the desired format
#         if len(parts) >= 5:  # Adjust this number if your folder structure is different
#             # Construct the new file name
#             new_name = f"arpa-{parts[1].split('-')[-2]}-{parts[1].split('-')[-1]}-{parts[-3]}-{parts[-2]}-{file.stem}.pdf"
#             new_file_path = file.with_name(new_name)

#             # Rename the file
#             file.rename(new_file_path)
#             total_files += 1
#             print(f"Renamed: {file} to {new_file_path}")

# # Start the search and renaming process
# find_and_rename_files(root_dir)
# print(f"Total PDF files renamed: {total_files}")

# from pathlib import Path

# # Define the root directory
# root_dir = Path("./data/arpa-orders-sample")
# total_files = 0

# def find_and_print_file_parts(dir_path):
#     global total_files
#     for file in dir_path.rglob("*.pdf"):  # Recursively find .pdf files
#         # Extract relevant parts of the path
#         parts = file.relative_to(root_dir).parts
        
#         # Print each part of the path for inspection
#         print(f"\nOriginal file path: {file}")
#         print(f"Relative parts from root directory '{root_dir}':")

#         new_name = f"arpa-{parts[0].split('-')[3]}-{parts[0].split('-')[4]}-{parts[2]}-{parts[3]}-{parts[4]}"

#         print(f"File name: {new_name}")
#         file.rename(new_name)


#         # Increment total file counter
#         total_files += 1

# # Start the search and part inspection process
# find_and_print_file_parts(root_dir)
# print(f"\nTotal PDF files found: {total_files}")

# working code for renameing pdf files
# from pathlib import Path

# # Define the root directory
# root_dir = Path("./data/arpa-orders-sample")
# total_files = 0

# def find_and_rename_files(dir_path):
#     global total_files
#     for file in dir_path.rglob("*.pdf"):  # Recursively find .pdf files
#         # Extract relevant parts of the path
#         parts = file.relative_to(root_dir).parts
        
#         # Construct the new file name based on the parts
#         new_name = f"arpa-{parts[0].split('-')[3]}-{parts[0].split('-')[4]}-{parts[2]}-{parts[3]}-{parts[4]}"
        
#         # Check if the file name already matches the intended format
#         if file.name == new_name:
#             print(f"Skipping already renamed file: {file}")
#             continue  # Skip renaming if the file already matches the new name
        
#         # Define the new file path
#         new_file_path = file.with_name(new_name)
        
#         # Rename the file
#         file.rename(new_file_path)
#         total_files += 1
#         print(f"Renamed: {file} to {new_file_path}")

# # Start the search and renaming process
# find_and_rename_files(root_dir)
# print(f"\nTotal PDF files renamed: {total_files}")

# from pathlib import Path

# # Define the root directory
# root_dir = Path("./data/arpa-orders")
# total_files = 0

# def find_and_rename_files(dir_path):
#     global total_files
#     for file in dir_path.rglob("*"):  # Recursively find all files
#         if file.suffix not in {".pdf", ".txt"}:
#             continue  # Skip if the file is not .pdf or .txt
        
#         # Extract relevant parts of the path
#         parts = file.relative_to(root_dir).parts
        
#         # Construct the new file name based on the parts and retain the original extension
#         new_name = f"arpa-{parts[0].split('-')[3]}-{parts[0].split('-')[4]}-{parts[2]}-{parts[3]}-{parts[4].split('.')[0].split('-')[len(parts[4].split('.')[0].split('-'))-2]}-{parts[4].split('.')[0].split('-')[len(parts[4].split('.')[0].split('-'))-1]}{file.suffix}"
        
#         print(f"New file name: {new_name}")
#         print(f"file name: {file.name}")
#         # Check if the file name already matches the intended format
#         if file.name == new_name:
#             print(f"Skipping already renamed file: {file}")
#             continue  # Skip renaming if the file already matches the new name
        
#         # Define the new file path
#         new_file_path = file.with_name(new_name)
        
#         # Rename the file
#         file.rename(new_file_path)
#         total_files += 1
#         # print(f"Renamed: {file} to {new_file_path}")

# # Start the search and renaming process
# find_and_rename_files(root_dir)
# print(f"\nTotal PDF and TXT files renamed: {total_files}")


from pathlib import Path

# Define the root directory
root_dir = Path("./data/arpa-orders")
total_files = 0

def find_and_rename_files(dir_path):
    global total_files
    for file in dir_path.rglob("*"):  # Recursively find all files

        # Skip files in the 'results' folder
        if 'results' in file.parts:
            continue  # Skip processing files in 'results' folder

        if file.suffix not in {".pdf", ".txt"}:
            continue  # Skip if the file is not .pdf or .txt
        
        # Extract relevant parts of the path
        parts = file.relative_to(root_dir).parts
        
        try:
            # Construct the new file name based on the parts and retain the original extension
            # print(f"parts: {parts}")
            new_name = f"arpa-{parts[0].split('-')[3]}-{parts[0].split('-')[4]}-{parts[2]}-{parts[3]}-{parts[4].split('.')[0].split('-')[-2]}-{parts[4].split('.')[0].split('-')[-1]}{file.suffix}"
            
            #print(f"New file name: {new_name}")
            #print(f"file name: {file.name}")
            
            # Check if the file name already matches the intended format
            if file.name == new_name:
                #print(f"Skipping already renamed file: {file}")
                continue  # Skip renaming if the file already matches the new name
            
            # Define the new file path
            new_file_path = file.with_name(new_name)
            
            # Rename the file
            file.rename(new_file_path)
            total_files += 1
            #print(f"Renamed: {file} to {new_file_path}")
        
        except Exception as e:
            print(f"Failed to rename: {file}")
            print(f"File Path: {file}")
            print(f"Error: {e}")

# Start the search and renaming process
find_and_rename_files(root_dir)
print(f"\nTotal PDF and TXT files renamed: {total_files}")
