import os
import shutil

def move_txt_files(source_dir, destination_dir):
    """
    Moves all .txt files from source_dir and its subdirectories to destination_dir,
    except for specific files.

    :param source_dir: The root directory to search for .txt files.
    :param destination_dir: The directory to move the .txt files to.
    """
    # List of files to exclude
    excluded_files = [
        "creating_directory_error_logs.txt",
        "downloading_pdf_error_logs.txt",
        "fetching_html_error_logs.txt",
        "query_error_logs.txt",
        "uploading_to_s3_error_logs.txt"
    ]

    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Walk through all subdirectories in the source directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.txt') and file not in excluded_files:
                # Construct full file paths
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_dir, file)

                # Ensure unique filenames in destination directory
                counter = 1
                while os.path.exists(destination_path):
                    base, ext = os.path.splitext(file)
                    destination_path = os.path.join(destination_dir, f"{base}_{counter}{ext}")
                    counter += 1

                # Move the file
                shutil.move(source_path, destination_path)
                print(f"Moved: {source_path} -> {destination_path}")

# Example usage
source_directory = "arpa-orders"
destination_directory = "txts"

move_txt_files(source_directory, destination_directory)
