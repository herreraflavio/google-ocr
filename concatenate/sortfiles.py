import os
from google.cloud import storage
import json
import time

# Replace 'file.txt' with the path to your text file
file_path_name = 'output.txt'
output_directory = "outputDirectory"

def read_json_from_gcs_and_save(bucket_name, file_path, output_txt_file):
    """Reads a JSON file from a GCP bucket and saves its content to a text file.

    Args:
        bucket_name (str): The name of the GCP bucket.
        file_path (str): The path to the JSON file in the bucket.
        output_txt_file (str): The path to the output .txt file.
    """
    start_time = time.time()  # Start timing

    # Initialize the Google Cloud Storage client
    client = storage.Client()

    # Get the bucket and blob
    bucket = client.get_bucket(bucket_name)
    print(file_path.split("/")[4])
    new_file_path = os.path.join(output_txt_file, file_path.split("/")[4])

    blob = bucket.blob(file_path)

    # Read the content of the blob as a string
    json_data = blob.download_as_text()

    # Ensure the directory exists
    print(output_txt_file)
    os.makedirs(output_txt_file, exist_ok=True)

    # Save the JSON content to a text file
    print(new_file_path)
    try:
        # Parse the JSON string into a Python dictionary
        parsed_data = json.loads(json_data)

        # Save the dictionary as JSON to the file
        with open(new_file_path, "w", encoding="utf-8") as json_file:
            json.dump(parsed_data, json_file, indent=4)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON from file {file_path}: {e}")

    end_time = time.time()  # End timing
    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"JSON content saved to {new_file_path}")
    print(f"Time taken: {elapsed_time_ms:.2f} ms")

# Usage example
bucket_name = "testbucketarpa"

try:
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    with open(file_path_name, 'r') as file:
        for i, line in enumerate(file):
            if i >= 19000:  # Stop after reading 100 lines
                break
            if i > 300:
                file_path = line.strip()
                split_items_list = line.split("/")
                if split_items_list[2].strip() != ".gitkeep":
                    # split_items_name_list = split_items_list[4].split("-")
                    # result = "-".join(split_items_name_list[:7]) 
                    
                    result = split_items_list[4].strip()
                    # print(result)
                    #output_directory = os.path.join("outputDirectory", result)
                    
                    # print(split_items_name_list[0])
                    
                    split_items_name_list = result.split("-")
                    output_result = "-".join(split_items_name_list[:7]) 

                    output_json_file = os.path.join(output_directory, output_result)
                    #print(file_path)
                    #print(output_json_file)
                    read_json_from_gcs_and_save(bucket_name, file_path, output_json_file)
                else:
                    print("================.gitkeep file encountered================")

except FileNotFoundError:
    print(f"The file at '{file_path_name}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
