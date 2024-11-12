import os

# Define the base directory where folders are created
base_directory = "./data/arpa-orders-output"  # Replace with your desired path
base_folder_name = "batch_"
total_folders = 738

# Create each folder from batch_1 to batch_738 in the specified directory
for i in range(1, total_folders + 1):
    folder_name = os.path.join(base_directory, f"{base_folder_name}{i}")
    os.makedirs(folder_name, exist_ok=True)  # Create folder if it doesn't exist
    print(f"Created folder: {folder_name}")

    # Check if the folder is empty
    if not os.listdir(folder_name):  # If the folder is empty
        gitkeep_path = os.path.join(folder_name, ".gitkeep")
        with open(gitkeep_path, "w") as f:
            pass  # Create an empty .gitkeep file
        print(f"Added .gitkeep to empty folder: {folder_name}")
