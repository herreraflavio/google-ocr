import os
import json

# Load the JSON array of folder names
json_file_path = 'unique_folders.json'

with open(json_file_path, 'r') as f:
    folder_list = json.load(f)

# Specify the base directory path where the folders are located
base_directory_path = './data/batches'

# Initialize an empty list to store folders that contain files with a second number greater than 500
folders_with_large_numbers = []

# Traverse each folder in the JSON array
for folder_name in folder_list:
    folder_path = os.path.join(base_directory_path, folder_name)
    
    # Check if the folder exists
    if os.path.isdir(folder_path):
        # Traverse all files in the folder
        for file_name in os.listdir(folder_path):
            # Check if the file name follows the expected pattern
            parts = file_name.split('-')
            
            # Check if the file name has at least three parts and if the third part is numeric
            if len(parts) > 2 and parts[2].isdigit():
                # Convert the third item (second number) to an integer
                second_number = int(parts[2])
                
                # Check if the second number is greater than 500
                if second_number > 500:
                    # Add the folder name to the list and break the loop if we find a match
                    folders_with_large_numbers.append(folder_name)
                    break

# Output the folders that contain files with a second number greater than 500
output_file = 'folders_with_large_numbers.json'
with open(output_file, 'w') as f:
    json.dump(folders_with_large_numbers, f, indent=4)

print(f"Folders with files having a second number > 500 saved to {output_file}")
