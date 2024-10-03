import re
import os
from dotenv import load_dotenv

from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import InternalServerError, RetryError
from google.cloud import documentai, storage

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")  # Format is 'us' or 'eu'
PROCESSOR_ID = os.getenv("PROCESSOR_ID")  # Create processor in Cloud Console

GCS_TEST_OUTPUT_URI = os.getenv("GCS_TEST_OUTPUT_URI")
GCS_TEST_INPUT_URI = os.getenv("GCS_TEST_INPUT_URI")

# TODO(developer): Fill these variables before running the sample.
project_id = PROJECT_ID
location = LOCATION  # Format is "us" or "eu"
processor_id = PROCESSOR_ID  # Create processor before running sample
gcs_output_uri = GCS_TEST_OUTPUT_URI  # Must end with a trailing slash `/`. Format: gs://bucket/directory/
input_mime_type = "application/pdf"
field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.
gcs_input_prefix = GCS_TEST_INPUT_URI  # The GCS directory containing your PDFs


def batch_process_documents_by_directory(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_input_prefix: str,  # Directory prefix in GCS
    gcs_output_uri: str,
    processor_version_id: str = None,
    input_mime_type: str = "application/pdf",
    field_mask: str = None,
    timeout: int = 400,
):
    # You must set the api_endpoint if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # Process all files in the directory using GcsPrefix
    gcs_prefix = documentai.GcsPrefix(gcs_uri_prefix=gcs_input_prefix)
    input_config = documentai.BatchDocumentsInputConfig(gcs_prefix=gcs_prefix)

    # Cloud Storage URI for the Output Directory
    gcs_output_config = documentai.DocumentOutputConfig.GcsOutputConfig(
        gcs_uri=gcs_output_uri, field_mask=field_mask
    )
    output_config = documentai.DocumentOutputConfig(gcs_output_config=gcs_output_config)

    # Build the processor name path
    if processor_version_id:
        name = client.processor_version_path(project_id, location, processor_id, processor_version_id)
    else:
        name = client.processor_path(project_id, location, processor_id)

    request = documentai.BatchProcessRequest(
        name=name,
        input_documents=input_config,
        document_output_config=output_config,
    )

    # BatchProcess returns a Long Running Operation (LRO)
    operation = client.batch_process_documents(request)

    # Poll the operation until it's done
    try:
        print(f"Waiting for operation {operation.operation.name} to complete...")
        operation.result(timeout=timeout)
    except (RetryError, InternalServerError) as e:
        print(f"Error during processing: {e.message}")

    # Once the operation is complete, get the output document information from the metadata
    metadata = documentai.BatchProcessMetadata(operation.metadata)

    if metadata.state != documentai.BatchProcessMetadata.State.SUCCEEDED:
        raise ValueError(f"Batch Process Failed: {metadata.state_message}")

    storage_client = storage.Client()

    print("Output files:")
    # One process per Input Document
    for process in metadata.individual_process_statuses:
        matches = re.match(r"gs://(.*?)/(.*)", process.output_gcs_destination)
        if not matches:
            print(f"Could not parse output GCS destination: {process.output_gcs_destination}")
            continue

        output_bucket, output_prefix = matches.groups()

        # Get List of Document Objects from the Output Bucket
        output_blobs = storage_client.list_blobs(output_bucket, prefix=output_prefix)

        # Document AI may output multiple JSON files per source file
        for blob in output_blobs:
            if blob.content_type != "application/json":
                print(f"Skipping non-supported file: {blob.name} - Mimetype: {blob.content_type}")
                continue

            # Download JSON File as bytes object and convert to Document Object
            print(f"Fetching {blob.name}")
            document = documentai.Document.from_json(blob.download_as_bytes(), ignore_unknown_fields=True)

            # Read the text recognition output from the processor
            print("The document contains the following text:")
            print(document.text)


if __name__ == "__main__":
    batch_process_documents_by_directory(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        gcs_input_prefix=gcs_input_prefix,  # Directory of PDFs in GCS
        gcs_output_uri=gcs_output_uri,  # Output directory for processed results
        input_mime_type=input_mime_type,
        field_mask=field_mask
    )
