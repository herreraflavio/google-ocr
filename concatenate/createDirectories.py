import os

# Replace 'file.txt' with the path to your text file
file_path = 'output.txt'
output_directory = "outputDirectory"

try:
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if i >= 100:  # Stop after reading 100 lines
                break

            split_items = line.strip()

            split_items_list = split_items.split("/")

            if split_items_list[2] != ".gitkeep":
                print(line.strip())
                # Combine the first 9 items
                split_items_name_list = split_items_list[4].split("-")
                result = "-".join(split_items_name_list[:7]) 

                # Create a new directory with the name `result` inside the output directory
                result_directory = os.path.join(output_directory, result)
                os.makedirs(result_directory, exist_ok=True)

                print(f"Created directory: {result_directory}")
                # print(result)
except FileNotFoundError:
    print(f"The file at '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
