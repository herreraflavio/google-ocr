import os
from bs4 import BeautifulSoup

def extract_text_from_html_files(source_dir, output_dir):
    """
    Reads each .txt file in the source_dir, treats its content as HTML, extracts
    visible text using BeautifulSoup, and writes the output to a new file in output_dir.

    :param source_dir: The directory containing the original .txt files.
    :param output_dir: The directory to store the output files.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Walk through all files in the source directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.txt'):
                # Construct full file paths
                source_path = os.path.join(root, file)
                output_path = os.path.join(output_dir, file)

                # Read the content of the original file
                with open(source_path, 'r', encoding='utf-8') as infile:
                    html_content = infile.read()

                # Parse the HTML content
                soup = BeautifulSoup(html_content, "html.parser")

                # Remove non-visible tags
                for element in soup(["script", "style"]):
                    element.decompose()

                # Extract visible text
                visible_text = soup.get_text(separator="\n", strip=True)

                # Write the visible text to a new file in the output directory
                with open(output_path, 'w', encoding='utf-8') as outfile:
                    outfile.write(visible_text)

                print(f"Extracted and saved: {source_path} -> {output_path}")

# Example usage
source_directory = "txts"
output_directory = "output_txt"

extract_text_from_html_files(source_directory, output_directory)
