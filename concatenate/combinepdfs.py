import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def extract_index(file_name):
    """
    Extract the last number after splitting the file name by '-'.

    Args:
        file_name (str): The name of the file.

    Returns:
        int: The extracted index as an integer.
    """
    try:
        return int(file_name.split('-')[-1].split('.')[0])  # Extract the index
    except ValueError:
        return float('inf')  # Return infinity if no valid number is found


def add_metadata_to_page(reader, writer, file_name):
    """
    Add metadata (original file name) as a new page overlay to each page of the PDF.

    Args:
        reader (PdfReader): Reader for the source PDF.
        writer (PdfWriter): Writer for the combined PDF.
        file_name (str): The original file name.
    """
    for page in reader.pages:
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 10)
        can.drawString(10, 10, f"Source File: {file_name}")  # Add metadata at the bottom left
        can.save()
        packet.seek(0)

        # Create a new PDF with the metadata
        overlay_reader = PdfReader(packet)
        overlay_page = overlay_reader.pages[0]
        page.merge_page(overlay_page)  # Overlay metadata onto the original page
        writer.add_page(page)


def process_folders(input_folder, output_folder):
    """
    Process each folder inside the input folder, combine sorted PDFs into a single PDF,
    and store them in the output folder.

    Args:
        input_folder (str): The path to the input folder containing subfolders of PDFs.
        output_folder (str): The path to the output folder where combined PDFs will be stored.
    """
    os.makedirs(output_folder, exist_ok=True)

    for root, dirs, _ in os.walk(input_folder):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            output_pdf_path = os.path.join(output_folder, f"{subdir}.pdf")

            # Get all PDF files in the subdirectory
            pdf_files = [f for f in os.listdir(subdir_path) if f.endswith('.pdf')]
            sorted_files = sorted(pdf_files, key=extract_index)

            writer = PdfWriter()
            for pdf_file in sorted_files:
                file_path = os.path.join(subdir_path, pdf_file)
                reader = PdfReader(file_path)
                add_metadata_to_page(reader, writer, pdf_file)

            # Save the combined PDF
            with open(output_pdf_path, 'wb') as output_pdf:
                writer.write(output_pdf)

            print(f"Combined PDF saved at: {output_pdf_path}")


# Example usage
input_folder = r"outputDirectory_extracted"  # Replace with the path to your input folder
output_folder = r"outputpdfs"  # Replace with the path to your output folder

process_folders(input_folder, output_folder)
