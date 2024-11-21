# from google.cloud import storage
# import json

# def read_json_from_gcs(bucket_name, file_path):
#     """Reads a JSON file from a GCP bucket without downloading it.

#     Args:
#         bucket_name (str): The name of the GCP bucket.
#         file_path (str): The path to the JSON file in the bucket.

#     Returns:
#         dict: The parsed JSON content.
#     """
#     # Initialize the Google Cloud Storage client
#     client = storage.Client()

#     # Get the bucket and blob
#     bucket = client.get_bucket(bucket_name)
#     blob = bucket.blob(file_path)

#     # Read the content of the blob as a string
#     json_data = blob.download_as_text()

#     # Parse the JSON content
#     return json.loads(json_data)

# # Usage example
# bucket_name = "testbucketarpa"
# file_path = "arpa-orders-output/batch_35/3459917010857088773/0/arpa-1-250-folder131-query1-file130-1-0.json"

# # Call the function and print the JSON content
# json_content = read_json_from_gcs(bucket_name, file_path)
# print(json_content)
from google.cloud import storage
import json
import time

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
    blob = bucket.blob(file_path)

    # Read the content of the blob as a string
    json_data = blob.download_as_text()

    # Save the JSON content to a text file
    with open(output_txt_file, "w", encoding="utf-8") as txt_file:
        txt_file.write(json_data)

    end_time = time.time()  # End timing
    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"JSON content saved to {output_txt_file}")
    print(f"Time taken: {elapsed_time_ms:.2f} ms")

# Usage example
bucket_name = "testbucketarpa"
file_path = "arpa-orders-output/batch_35/3459917010857088773/0/arpa-1-250-folder131-query1-file130-1-3.json"
output_txt_file = "jsonoutput.txt"

# Call the function
read_json_from_gcs_and_save(bucket_name, file_path, output_txt_file)
