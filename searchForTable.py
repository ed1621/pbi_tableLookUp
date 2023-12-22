# STEP 4 of 5:
#
# This will parse the txt file of data character by character (because of formatting)
# To see if a specific string (Table Name) is found (ex FactSales)
# It will then create a txt file with the reports that are currently using the string (Table Name)

import os
import re

# Function to check if a specific phrase is present in the layout file
def check_layout_for_phrase(layout_path, search_phrase):
    try:
        with open(layout_path, 'r', encoding='utf-8') as layout_file:
            # Read the layout file
            layout_content = layout_file.read()

        # Remove non-alphanumeric characters and convert to lowercase
        # This is added because the returned text file has an obscure formatting issue
        # That doesn't read well on plain text UTF-8 or JSON. This fixes it to read
        # Through the file correctly and spot the Table Name.
        cleaned_layout = re.sub(r'[^a-zA-Z0-9]', '', layout_content).lower()
        cleaned_search_phrase = re.sub(r'[^a-zA-Z0-9]', '', search_phrase).lower()

        # Check if the cleaned search phrase is present in the cleaned layout content
        return cleaned_search_phrase in cleaned_layout
    except FileNotFoundError:
        pass  # Handle the case where the Layout file is not found

    return False

# Folder paths
unzipped_folder = r'pah to unzipped files folder'
desktop_path = r"Path to where you want the results txt file to go"
result_file_path = os.path.join(desktop_path, "SearchResults.txt")

# Search phrase input
search_phrase = input("Enter the table name to search for: ")

# Clear the result file before running the script
open(result_file_path, 'w').close()

# Iterate through folders in the unzipped folder
for report_folder in os.listdir(unzipped_folder):
    report_folder_path = os.path.join(unzipped_folder, report_folder)

    # Check if the path is a directory
    if os.path.isdir(report_folder_path):
        # Look for the "Report" folder and "Layout" file
        layout_path = os.path.join(report_folder_path, 'Report', 'Layout_Content.txt')

        # Check if the search phrase is present in the Layout file
        is_present = check_layout_for_phrase(layout_path, search_phrase)

        # Write results to the text file only if the search phrase is found
        if is_present:
            with open(result_file_path, 'a') as file:
                file.write(f"Report: {report_folder}, {search_phrase} Present: {str(is_present)}\n")

print(f"Results written to: {result_file_path}")

