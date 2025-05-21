# Zip Files from pbix file - version 1
# Benjamin Leanna 2023-12-21
#
# STEP 1 of 5:
#
# Change the input folder below to the correct path
# example: r'V:\Reporting\Power BI\Reports\CORPORATE' will look in the
# corporate forlder for the reports. This file will transform them into ZIP files
# This doesn't compress them but rather convert them.

import os
import zipfile
import tempfile
import shutil
import re

# Function to convert PBIX to ZIP
def convert_pbix_to_zip(pbix_path, output_folder):
    pbix_filename = os.path.basename(pbix_path)
    zip_filename = os.path.splitext(pbix_filename)[0] + ".zip"
    zip_path = os.path.join(output_folder, zip_filename)

    # Create a temporary directory to extract the PBIX contents
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract the contents of the PBIX file to the temporary directory
        with zipfile.ZipFile(pbix_path, 'r') as pbix_zip:
            pbix_zip.extractall(temp_dir)

        # Compress the extracted contents into a new ZIP file
        shutil.make_archive(zip_path, 'zip', temp_dir)

    return zip_path

# Folder paths
input_folder = r'path to where your power bi reports are'
output_folder = r'path to where you want the zipped files to be'
print("Converting PBIX Files to ZIP files. This may take a minute depending on number of Reports....")
# Iterate through PBIX files in the input folder (only taking PBIX files)
for pbix_file in os.listdir(input_folder):
    if pbix_file.endswith('.pbix'):
        pbix_path = os.path.join(input_folder, pbix_file)

        # Convert PBIX to ZIP
        zip_path = convert_pbix_to_zip(pbix_path, output_folder)

###################################################################################
# STEP 2 of 5:
#
# This file will now unzip all of the files and put them into a new folder.


# Function to unzip all ZIP files in a folder
def unzip_all_files(input_folder, output_folder):
    print(f"Input folder contents before extraction: {os.listdir(input_folder)}")

    for zip_file in os.listdir(input_folder):
        if zip_file.endswith('.zip'):
            zip_path = os.path.join(input_folder, zip_file)
            unzip_folder = os.path.join(output_folder, os.path.splitext(zip_file)[0])

            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(unzip_folder)
                print(f"Extraction complete for {zip_file}")
            except Exception as e:
                print(f"Error extracting {zip_file}: {e}")

    print("All extractions complete.")

# Folder paths
input_folder = r'path to where the zip files are'
output_folder = r'path to where you want the unzipped files to be'

print("Starting the unzip process...")
# Unzip all files in the input folder to separate folders in the output folder
unzip_all_files(input_folder, output_folder)
print("Unzip process completed.")
print("\n")
print("\n")
######################################################################################
# STEP 3 of 5:
#
# This will now convert all of the Layoutfiles within the unzipped folders
# to TXT files so that we can parse them for a table name.


# Function to print the content of the layout file to a text file
def print_layout_content(layout_path, output_file):
    try:
        with open(layout_path, 'r', encoding='ISO-8859-1') as layout_file, open(output_file, 'w', encoding='utf-8') as output:
            layout_content = layout_file.read()
            output.write(layout_content)
    except FileNotFoundError:
        pass  # Handle the case where the Layout file is not found

# Folder paths
unzipped_folder = r'path to where unzipped files are'

# Iterate through folders in the unzipped folder
for report_folder in os.listdir(unzipped_folder):
    report_folder_path = os.path.join(unzipped_folder, report_folder)

    # Check if the path is a directory
    if os.path.isdir(report_folder_path):
        # Look for the "Report" folder and "Layout" file
        layout_path = os.path.join(report_folder_path, 'Report', 'Layout')

        # Specify the output file path in the Report folder
        output_file = os.path.join(report_folder_path, 'Report', 'Layout_Content.txt')

        # Print the content of the Layout file to the output text file
        print_layout_content(layout_path, output_file)

########################################################################################

# STEP 4 of 5:
#
# This will parse the txt file of data character by character (because of formatting)
# To see if a specific string (Table Name) is found (ex FactSales)
# It will then create a txt file with the reports that are currently using the string (Table Name)


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
unzipped_folder = r'path to where unzipped files are'
desktop_path = r"path to where you want search results to be"
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

