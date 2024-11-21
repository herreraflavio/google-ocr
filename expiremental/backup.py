import concurrent.futures
import urllib.request
import re

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

    # Improved function to handle logging of errors
    # Base logging functions
    def log_error(message):
        with open("./logs/errors.txt", "a") as error_file:
            error_file.write(message + "\n")

    def log_error_path(message, extra_data=None):
        with open("./logs/errors.txt", "a") as error_file:
            error_file.write(message + "\n")
            if extra_data:
                for key, value in extra_data.items():
                    error_file.write(f"{key}: {value}\n")

    print("Output files:")

    # Process each input document's output GCS destination
    for process in list(metadata.individual_process_statuses):
        # Expect format: gs://BUCKET/PREFIX/OPERATION_NUMBER/INPUT_FILE_NUMBER/
        output_gcs_destination = process.output_gcs_destination or "N/A"
        document_id = process.input_gcs_source or "N/A"  # Unique identifier for each document

        # Log the output destination and check if it's empty or invalid
        log_error_path("Processing document output destination", {
            "output_gcs_destination": output_gcs_destination,
            "document_id": document_id
        })
        
        # Updated regex to ensure we have a bucket and path, handling optional trailing slash
        matches = re.match(r"^gs://([^/]+)/(.*)$", output_gcs_destination)

        if not matches:
            # Detailed error handling for different scenarios
            error_type = ""
            if not output_gcs_destination or output_gcs_destination == "N/A":
                error_message = "Output GCS destination is missing or empty."
                error_type = "Missing Destination"
            elif not output_gcs_destination.startswith("gs://"):
                error_message = f"Invalid URI format, expected 'gs://': {output_gcs_destination}"
                error_type = "Invalid Format"
            elif output_gcs_destination.count('/') < 2:
                error_message = (
                    f"Incomplete URI. Expected format 'gs://bucket/path', got: {output_gcs_destination}"
                )
                error_type = "Incomplete URI"
            else:
                error_message = f"Could not parse output GCS destination: {output_gcs_destination}"
                error_type = "Parsing Error"

            # Log detailed error information
            print(error_message)
            log_error_path(error_message, {
                "output_gcs_destination": output_gcs_destination,
                "document_id": document_id,
                "error_type": error_type,
                "status_code": process.status.code if process.status else "N/A",
                "status_message": process.status.message if process.status else "N/A",
                "overall_batch_state": metadata.state if metadata.state else "N/A",
                "overall_batch_state_message": metadata.state_message if metadata.state_message else "N/A",
                "total_documents_in_batch": len(metadata.individual_process_statuses),
                "complete_metadata": str(metadata)  # Full metadata for comprehensive tracking
            })
            continue

        # Extract bucket and prefix from regex match
        output_bucket, output_prefix = matches.groups()
        print(f"Parsed output bucket: {output_bucket}, prefix: {output_prefix}")
        log_error_path("Parsed output details", {"output_bucket": output_bucket, "output_prefix": output_prefix})

        # Try to retrieve list of blobs in the output bucket, handling any errors with extensive logging
        try:
            output_blobs = storage_client.list_blobs(output_bucket, prefix=output_prefix)
        except Exception as e:
            error_message = f"Error accessing bucket '{output_bucket}' with prefix '{output_prefix}': {str(e)}"
            print(error_message)
            log_error_path(error_message, {
                "output_bucket": output_bucket,
                "output_prefix": output_prefix,
                "document_id": document_id,
                "error_details": str(e)
            })
            continue

        # Process each blob in the output
        for blob in output_blobs:
            # Only process JSON files
            if blob.content_type != "application/json":
                warning_message = f"Skipping non-supported file: {blob.name} - Mimetype: {blob.content_type}"
                print(warning_message)
                log_error_path(warning_message, {"blob_name": blob.name, "content_type": blob.content_type})
                continue

            # Fetch and process JSON content
            print(f"Fetching {blob.name}")
            log_error_path("Fetching blob", {"blob_name": blob.name})

            try:
                # Decode with UTF-8 to handle special characters like '\u25a0'
                document_content = blob.download_as_bytes().decode('utf-8')
                document = documentai.Document.from_json(document_content, ignore_unknown_fields=True)
                
                # Display partial text for confirmation
                print("The document has been processed")
                print(document.text[:100])
                log_error_path("Document processed successfully", {
                    "blob_name": blob.name,
                    "document_text_snippet": document.text[:100]
                })
            except UnicodeEncodeError as e:
                # Handle Unicode encoding errors with detailed logging
                error_message = f"Unicode encoding error processing document from blob: {blob.name}"
                print(error_message)
                log_error_path(error_message, {
                    "blob_name": blob.name,
                    "error_details": str(e),
                    "content_snippet": document_content[:200]  # Log a snippet of the problematic content
                })

if __name__ == "__main__":
    # Generate 20 input and output URIs for batches
    input_uris = [f"{GCS_INPUT_URI}/batch_{i}/" for i in range(76, 78)]
    output_uris = [f"{GCS_OUTPUT_URI}/batch_{i}/" for i in range(76, 78)]
    
    log_error("error logs will go here: ")
    
    # Print all input URIs for reference
    for uri in input_uris:
        print(f"Input URI: {uri}")
    
    # Use ThreadPoolExecutor with max_workers=5 to keep 5 batches processing at a time
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_to_uri = {}  # Track futures and their associated URIs
        uri_index = 0  # Index for tracking which batch to start next

        # Start initial 5 batches
        for _ in range(2):
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
