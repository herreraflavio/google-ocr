import re
import os
from dotenv import load_dotenv
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import InternalServerError, RetryError
from google.cloud import documentai, storage
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")  # Format is 'us' or 'eu'
PROCESSOR_ID = os.getenv("PROCESSOR_ID")
GCS_OUTPUT_URI = os.getenv("GCS_BATCH_OUTPUT_URI")
GCS_INPUT_URI = os.getenv("GCS_BATCH_INPUT_URI")

input_uris = [f"{GCS_INPUT_URI}/{i}" for i in range(1, 6)]  # List of input files for 5 batch requests

for uri in input_uris:
    print(f"Input URI: {uri}")

print(f"Input URIs: {GCS_INPUT_URI}")

def batch_process_documents(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_input_uri: str,
    gcs_output_uri: str,
    processor_version_id: str = None,
    input_mime_type: str = None,
    field_mask: str = None,
    timeout: int = 1000,
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

    # The full resource name of the processor, e.g.:
    name = client.processor_path(project_id, location, processor_id)

    request = documentai.BatchProcessRequest(
        name=name,
        input_documents=input_config,
        document_output_config=output_config,
    )

    # BatchProcess returns a Long Running Operation (LRO)
    operation = client.batch_process_documents(request)

    # Continually polls the operation until it is complete.
    try:
        print(f"Waiting for operation {operation.operation.name} to complete...")
        operation.result(timeout=timeout)
    except (RetryError, InternalServerError) as e:
        print(e.message)

    # Once the operation is complete, get output document information from operation metadata
    metadata = documentai.BatchProcessMetadata(operation.metadata)

    if metadata.state != documentai.BatchProcessMetadata.State.SUCCEEDED:
        raise ValueError(f"Batch Process Failed: {metadata.state_message}")

    storage_client = storage.Client()

    print("Output files:")
    # One process per Input Document
    for process in list(metadata.individual_process_statuses):
        # output_gcs_destination format: gs://BUCKET/PREFIX/OPERATION_NUMBER/INPUT_FILE_NUMBER/
        matches = re.match(r"gs://(.*?)/(.*)", process.output_gcs_destination)
        if not matches:
            print(
                "Could not parse output GCS destination:",
                process.output_gcs_destination,
            )
            continue

        output_bucket, output_prefix = matches.groups()
        output_blobs = storage_client.list_blobs(output_bucket, prefix=output_prefix)

        for blob in output_blobs:
            if blob.content_type != "application/json":
                print(f"Skipping non-supported file: {blob.name} - Mimetype: {blob.content_type}")
                continue

            print(f"Fetching {blob.name}")
            document = documentai.Document.from_json(
                blob.download_as_bytes(), ignore_unknown_fields=True
            )

            print("The document contains the following text:")
            print(document.text)


def process_in_parallel():
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(batch_process_documents, 
                                   PROJECT_ID, LOCATION, PROCESSOR_ID, 
                                   uri, GCS_OUTPUT_URI) 
                   for uri in input_uris]
        for future in as_completed(futures):
            try:
                future.result()  # This will raise any exceptions caught during execution
            except Exception as e:
                print(f"Batch request failed: {e}")


if __name__ == "__main__":
    process_in_parallel()
