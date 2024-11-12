import concurrent.futures
import urllib.request

"""
Makes a Batch Processing Request to Document AI
"""

import re
import os
from dotenv import load_dotenv

from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import RetryError
from google.cloud import documentai
from google.cloud import storage

# Load environment variables from .env file
load_dotenv()

# PROJECT_ID = os.getenv("PROJECT_ID")
# LOCATION = os.getenv("LOCATION")  # Format is 'us' or 'eu'
# PROCESSOR_ID = os.getenv("PROCESSOR_ID")  # Create processor in Cloud Console

# GCS_OUTPUT_URI = os.getenv("GCS_BATCH_OUTPUT_URI")
# GCS_INPUT_URI = os.getenv("GCS_BATCH_INPUT_URI")
PROJECT_ID = "437973525643"
LOCATION = "us"  # Format is 'us' or 'eu'
PROCESSOR_ID = "822f416532363e58"  # Create processor in Cloud Console

GCS_OUTPUT_URI = "gs://testbucketarpa/arpa-orders-output"
GCS_INPUT_URI = "gs://testbucketarpa/arpa-orders"


# TODO(developer): Fill these variables before running the sample.
project_id = PROJECT_ID
location = LOCATION  # Format is "us" or "eu"
processor_id = PROCESSOR_ID  # Create processor before running sample
gcs_output_uri = GCS_OUTPUT_URI  # Must end with a trailing slash `/`. Format: gs://bucket/directory/subdirectory/
processor_version_id = (
    "YOUR_PROCESSOR_VERSION_ID"  # Optional. Example: pretrained-ocr-v1.0-2020-09-23
)

# TODO(developer): If `gcs_input_uri` is a single file, `mime_type` must be specified.
gcs_input_uri = GCS_INPUT_URI  # Format: `gs://bucket/directory/file.pdf` or `gs://bucket/directory/`
input_mime_type = "application/pdf"
field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.

# Ensure the logs directory exists
os.makedirs("./logs", exist_ok=True)

# Function to write errors to log file
def log_error(message):
    with open("./logs/errors.txt", "a") as error_file:
        error_file.write(message + "\n")

def batch_process_documents(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_input_uri: str,
    gcs_output_uri: str,
    processor_version_id: str = None,
    input_mime_type: str = None,
    field_mask: str = None,
    timeout: int = 3600,
):
    # You must set the api_endpoint if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    if not gcs_input_uri.endswith("/") and "." in gcs_input_uri:
        # Specify specific GCS URIs to process individual documents
        gcs_document = documentai.GcsDocument(
            gcs_uri=gcs_input_uri, mime_type=input_mime_type
        )
        # Load GCS Input URI into a List of document files
        gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
        input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)
    else:
        # Specify a GCS URI Prefix to process an entire directory
        gcs_prefix = documentai.GcsPrefix(gcs_uri_prefix=gcs_input_uri)
        input_config = documentai.BatchDocumentsInputConfig(gcs_prefix=gcs_prefix)

    # Cloud Storage URI for the Output Directory
    gcs_output_config = documentai.DocumentOutputConfig.GcsOutputConfig(
        gcs_uri=gcs_output_uri, field_mask=field_mask
    )

    # Where to write results
    output_config = documentai.DocumentOutputConfig(gcs_output_config=gcs_output_config)

    if processor_version_id:
        # The full resource name of the processor version, e.g.:
        # projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}
        name = client.processor_version_path(
            project_id, location, processor_id, processor_version_id
        )
    else:
        # The full resource name of the processor, e.g.:
        # projects/{project_id}/locations/{location}/processors/{processor_id}
        name = client.processor_path(project_id, location, processor_id)

    request = documentai.BatchProcessRequest(
        name=name,
        input_documents=input_config,
        document_output_config=output_config,
    )

    # BatchProcess returns a Long Running Operation (LRO)
    operation = client.batch_process_documents(request)

    # Continually polls the operation until it is complete.
    # This could take some time for larger files
    # Format: projects/{project_id}/locations/{location}/operations/{operation_id}
    try:
        print(f"Waiting for operation {operation.operation.name} to complete...")
        operation.result(timeout=timeout)
    # Catch exception when operation doesn"t finish before timeout
    except (RetryError, InternalServerError) as e:
        print(e.message)
        log_error(e.message)  # Log error to file

    # NOTE: Can also use callbacks for asynchronous processing
    #
    # def my_callback(future):
    #   result = future.result()
    #
    # operation.add_done_callback(my_callback)

    # Once the operation is complete,
    # get output document information from operation metadata
    metadata = documentai.BatchProcessMetadata(operation.metadata)

    if metadata.state != documentai.BatchProcessMetadata.State.SUCCEEDED:
        error_message = f"Batch Process Failed:  {metadata.state_message}"
        log_error(error_message)
        raise ValueError(f"Batch Process Failed: {metadata.state_message}")

    storage_client = storage.Client()

    print("Output files:")
    # One process per Input Document
    for process in list(metadata.individual_process_statuses):
        # output_gcs_destination format: gs://BUCKET/PREFIX/OPERATION_NUMBER/INPUT_FILE_NUMBER/
        # The Cloud Storage API requires the bucket name and URI prefix separately
        matches = re.match(r"gs://(.*?)/(.*)", process.output_gcs_destination)
        if not matches:
            error_message = f"Could not parse output GCS destination: { process.output_gcs_destination}"
            print(
              error_message
            )
            log_error(error_message)
            continue

        output_bucket, output_prefix = matches.groups()

        # Get List of Document Objects from the Output Bucket
        output_blobs = storage_client.list_blobs(output_bucket, prefix=output_prefix)

        # Document AI may output multiple JSON files per source file
        for blob in output_blobs:
            # Document AI should only output JSON files to GCS
            if blob.content_type != "application/json":
                warning_message =f"Skipping non-supported file: {blob.name} - Mimetype: {blob.content_type}"
                print(
                  warning_message
                )
                log_error(warning_message)  # Log error to file
                continue

            # Download JSON File as bytes object and convert to Document Object
            print(f"Fetching {blob.name}")
            document = documentai.Document.from_json(
                blob.download_as_bytes(), ignore_unknown_fields=True
            )

            # For a full list of Document object attributes, please reference this page:
            # https://cloud.google.com/python/docs/reference/documentai/latest/google.cloud.documentai_v1.types.Document

            # Read the text recognition output from the processor
            # print("The document contains the following text:")
            # print(document.text)
            print("The document has been processed")
            print(document.text[:100])


# if __name__ == "__main__":
#     # Define multiple input URIs to process concurrently

#     input_uris = [f"{GCS_INPUT_URI}/{i}" for i in range(1, 6)]  # List of input files for 5 batch requests
#     output_uris = [f"{GCS_OUTPUT_URI}/{i}" for i in range(1, 6)]  # List of output files for 5 batch requests
#     log_error("error logs will go here: ")
#     for uri in input_uris:
#         print(f"Input URI: {uri}")
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

#         # Start the load operations and mark each future with its URL
#         future_to_uri = {executor.submit(batch_process_documents, PROJECT_ID, LOCATION, PROCESSOR_ID, uri, output_uri): uri for uri, output_uri in zip(input_uris, output_uris)}

#         for future in concurrent.futures.as_completed(future_to_uri):
#             uri = future_to_uri[future]
#             try:
#                 future.result()
#                 print(f"Processing completed for {uri}")
#             except Exception as exc:
#                 error_message = f"Processing failed for {uri} with exception: {exc}"
#                 print(error_message)
#                 log_error(error_message)  # Log error to file

if __name__ == "__main__":
    # Generate 20 input and output URIs for batches
    input_uris = [f"{GCS_INPUT_URI}/batch_{i}" for i in range(1, 21)]
    output_uris = [f"{GCS_OUTPUT_URI}/batch_{i}" for i in range(1, 21)]
    
    log_error("error logs will go here: ")
    
    # Print all input URIs for reference
    for uri in input_uris:
        print(f"Input URI: {uri}")
    
    # Use ThreadPoolExecutor with max_workers=5 to keep 5 batches processing at a time
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_uri = {}  # Track futures and their associated URIs
        uri_index = 0  # Index for tracking which batch to start next

        # Start initial 5 batches
        for _ in range(5):
            future = executor.submit(
                batch_process_documents, PROJECT_ID, LOCATION, PROCESSOR_ID,
                input_uris[uri_index], output_uris[uri_index]
            )
            future_to_uri[future] = input_uris[uri_index]
            uri_index += 1
        
        # As each batch completes, start a new one until we reach 20 batches
        while future_to_uri:
            # As each future completes, process it and start a new batch if available
            for future in concurrent.futures.as_completed(future_to_uri):
                uri = future_to_uri.pop(future)  # Remove the completed future

                try:
                    future.result()
                    print(f"Processing completed for {uri}")
                except Exception as exc:
                    error_message = f"Processing failed for {uri} with exception: {exc}"
                    print(error_message)
                    log_error(error_message)  # Log error to file

                # Start the next batch if available
                if uri_index < len(input_uris):
                    next_future = executor.submit(
                        batch_process_documents, PROJECT_ID, LOCATION, PROCESSOR_ID,
                        input_uris[uri_index], output_uris[uri_index]
                    )
                    future_to_uri[next_future] = input_uris[uri_index]
                    uri_index += 1
