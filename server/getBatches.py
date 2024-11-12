import os
import json

# Specify the directory path
directory_path = './data/batches'

# Initialize an empty set to store unique folder names
unique_folders = set()


# Traverse through all files and folders
for root, dirs, files in os.walk(directory_path):
    for file_name in files:
        # Check if the file name follows the expected pattern
        parts = file_name.split('-')
        
        # Check if the file name has at least three parts and if the third part is numeric
        if len(parts) > 2 and parts[2].isdigit():
            # Convert the third item (second number) to an integer
            second_number = int(parts[2])
            
            # Check if the second number is less than or equal to 500
            if second_number <= 500:
                # Get the parent folder name (the last part of the root path)
                folder_name = os.path.basename(root)
                # Add the folder name to the set of unique values
                unique_folders.add(folder_name)
                
# Convert the set to a list
unique_folders_list = list(unique_folders)

# Specify the output JSON file path
output_file = 'unique_folders.json'

# Dump the list into a JSON file
with open(output_file, 'w') as f:
    json.dump(unique_folders_list, f, indent=4)

print(f"Unique folders saved to {output_file}")
