from google.cloud import storage

def list_all_file_paths(bucket_name, prefix=None, output_file='file_paths.txt'):
    # Initialize the client
    client = storage.Client()

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    # List all blobs (files) in the bucket
    blobs = bucket.list_blobs(prefix=prefix)

    # Open the output file in write mode
    with open(output_file, 'w') as file:
        for blob in blobs:
            # Write each file path to the output file
            file.write(blob.name + '\n')

    print(f"File paths have been saved to {output_file}")

# Replace 'testbucketarpa' with the name of your bucket
bucket_name = 'testbucketarpa'
# Replace 'arpa-orders-output/' with the folder path (if needed)
folder_path = 'arpa-orders-output/'  # Optional: folder prefix inside the bucket
list_all_file_paths(bucket_name, prefix=folder_path, output_file='output.txt')
