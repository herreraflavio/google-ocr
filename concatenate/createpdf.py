import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def extract_text_by_page(document_json):
    """
    Extracts the text from the Document AI JSON output and associates it with each page.

    Args:
    - document_json: JSON data from Google Document AI output.

    Returns:
    - A dictionary containing text for each page.
    """
    full_text = document_json['text']  # This contains the full text of the document
    full_text = full_text.replace("\n", " ")
    # Initialize the output dictionary
    output_data = []

    # Loop through each page in the document
    for page_num, page in enumerate(document_json['pages']):
        page_text = ""
        print(f"Processing page {page_num + 1}")

        # Check if 'blocks' exist in the page
        if not page.get('blocks', []):
            print(f"Page {page_num + 1} is empty. Creating an empty page.")
            output_data.append({
                "page_number": page_num + 1,
                "text": ""  # Add an empty page
            })
            continue

        # Loop through the blocks in each page
        for block in page['blocks']:
            # Extract text using the text segments (anchors) in the block layout
            if 'textAnchor' in block['layout'] and 'textSegments' in block['layout']['textAnchor']:
                for segment in block['layout']['textAnchor']['textSegments']:
                    start_idx = int(segment.get('startIndex', 0))  # Start index defaults to 0 if missing
                    end_idx = int(segment.get('endIndex', len(full_text)))  # End index defaults to the length of the text
                    page_text += full_text[start_idx:end_idx] + " "  # Add space between blocks for readability

        # Append text for the page
        output_data.append({
            "page_number": page_num + 1,
            "text": page_text.strip()  # Remove leading/trailing whitespace
        })

    return output_data

def save_text_to_pdf(extracted_data, output_pdf_path):
    """
    Saves the extracted text to a PDF, with each page's text on a separate page.

    Args:
    - extracted_data: List of dictionaries containing page text.
    - output_pdf_path: The path where the PDF will be saved.
    """
    # Create a new PDF with ReportLab
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    margin = 40  # Define a margin
    max_width = width - 2 * margin  # Maximum width for the text

    for page in extracted_data:
        page_text = page["text"]
        text_object = c.beginText(margin, height - margin)  # Starting position for text
        text_object.setFont("Helvetica", 12)  # Adjusted font size for better readability

        # Split text into lines based on page width
        words = page_text.split()
        line = ""
        for word in words:
            # Check if adding the word exceeds the width
            if c.stringWidth(line + " " + word, "Helvetica", 12) <= max_width:
                line += (" " if line else "") + word
            else:
                # Write the current line to the text object and start a new line
                text_object.textLine(line)
                line = word

        # Write any remaining text to the text object
        if line:
            text_object.textLine(line)

        # Draw the text object and move to the next page
        c.drawText(text_object)
        c.showPage()

    # Save the PDF file
    c.save()


def read_json_files_in_directory(directory):
    # List to store relative paths of JSON files
    json_file_paths = []
    
    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):  # Check if the file is a JSON file
                # Get the relative path of the JSON file
                relative_path = os.path.relpath(os.path.join(root, file), start=directory)
                json_file_paths.append(relative_path)
                
                # Open and read the JSON file
                try:
                    with open(os.path.join(root, file), "r", encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        outputDirectory_extracted_full = os.path.join("outputDirectory_extracted",relative_path.split("\\")[0])
                        print(outputDirectory_extracted_full)
                        
                        try:
                            os.makedirs(outputDirectory_extracted_full, exist_ok=True)
                            print(f"Directory '{outputDirectory_extracted_full}' is ready.")
                            base_name = os.path.splitext(os.path.basename(relative_path))[0]
                            new_path = os.path.join(outputDirectory_extracted_full, f"{base_name}.pdf")

                            print(new_path)

                            # Extract text by page
                            extracted_data = extract_text_by_page(data)
                            # print(extracted_data)
                            # Save the segmented text into a new PDF file
                            save_text_to_pdf(extracted_data,new_path)

                            print("Text segmented by page has been saved to output_document.pdf")
                        except Exception as e:
                            print(f"Error creating directory '{outputDirectory_extracted_full}': {e}")

                except Exception as e:
                    print(f"Error reading {relative_path}: {e}")
    
    # Return the list of relative paths
    return json_file_paths

# Example usage
directory_to_scan = "outputDirectory"  # Replace with your directory path
json_files = read_json_files_in_directory(directory_to_scan)

# def save_text_to_pdf(extracted_data, output_pdf_path):
#     """
#     Saves the extracted text to a PDF, with each page's text on a separate page.

#     Args:
#     - extracted_data: List of dictionaries containing page text.
#     - output_pdf_path: The path where the PDF will be saved.
#     """
#     # Create a new PDF with ReportLab
#     c = canvas.Canvas(output_pdf_path, pagesize=letter)
#     width, height = letter

#     for page in extracted_data:
#         page_text = page["text"]
#         text_object = c.beginText(40, height - 40)  # Starting position for text
#         text_object.setFont("Helvetica", 5)  # Set the font and size (e.g., 12 points)


#         # Add text to the page, wrapping lines if necessary
#         for line in page_text.splitlines():
#             text_object.textLine(line)

#         # Draw the text object and move to the next page
#         c.drawText(text_object)
#         c.showPage()

#     # Save the PDF file
#     c.save()

# Load the JSON file generated by Google Cloud Document AI
# with open('outputDirectory\\arpa-1-250-folder1-query1-file0-2\\arpa-1-250-folder1-query1-file0-2-0.json', 'r', encoding='utf-8') as file:
#     document_json = json.load(file)

# # Extract text by page
# extracted_data = extract_text_by_page(document_json)

# # Save the segmented text into a new PDF file
# save_text_to_pdf(extracted_data, 'output_document.pdf')

# print("Text segmented by page has been saved to output_document.pdf")


# print("\nList of JSON files with relative paths:")
# for path in json_files:
#     print(path)


# import json
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas

# def extract_text_by_page(document_json):
#     """
#     Extracts the text from the Document AI JSON output and associates it with each page.

#     Args:
#     - document_json: JSON data from Google Document AI output.

#     Returns:
#     - A dictionary containing text for each page.
#     """
#     full_text = document_json['text']  # This contains the full text of the document

#     # Initialize the output dictionary
#     output_data = []

#     # Loop through each page in the document
#     for page_num, page in enumerate(document_json['pages']):
#         page_text = ""

#         # Loop through the blocks in each page
#         for block in page['blocks']:
#             # Extract text using the text segments (anchors) in the block layout
#             if 'textAnchor' in block['layout'] and 'textSegments' in block['layout']['textAnchor']:
#                 for segment in block['layout']['textAnchor']['textSegments']:
#                     start_idx = int(segment.get('startIndex', 0))  # Start index defaults to 0 if missing
#                     end_idx = int(segment.get('endIndex', len(full_text)))  # End index defaults to the length of the text
#                     page_text += full_text[start_idx:end_idx] + " "  # Add space between blocks for readability

#         # Append text for the page
#         output_data.append({
#             "page_number": page_num + 1,
#             "text": page_text.strip()  # Remove leading/trailing whitespace
#         })

#     return output_data

# def save_text_to_pdf(extracted_data, output_pdf_path):
#     """
#     Saves the extracted text to a PDF, with each page's text on a separate page.

#     Args:
#     - extracted_data: List of dictionaries containing page text.
#     - output_pdf_path: The path where the PDF will be saved.
#     """
#     # Create a new PDF with ReportLab
#     c = canvas.Canvas(output_pdf_path, pagesize=letter)
#     width, height = letter

#     for page in extracted_data:
#         page_text = page["text"]
#         text_object = c.beginText(40, height - 40)  # Starting position for text
#         text_object.setFont("Helvetica", 5)  # Set the font and size (e.g., 12 points)


#         # Add text to the page, wrapping lines if necessary
#         for line in page_text.splitlines():
#             text_object.textLine(line)

#         # Draw the text object and move to the next page
#         c.drawText(text_object)
#         c.showPage()

#     # Save the PDF file
#     c.save()

# # Load the JSON file generated by Google Cloud Document AI
# with open('expiremental\\output\\output\\batch\\1\\707188629682975322\\0\\180-0.json', 'r', encoding='utf-8') as file:
#     document_json = json.load(file)

# # Extract text by page
# extracted_data = extract_text_by_page(document_json)

# # Save the segmented text into a new PDF file
# save_text_to_pdf(extracted_data, 'output_document.pdf')

# print("Text segmented by page has been saved to output_document.pdf")
