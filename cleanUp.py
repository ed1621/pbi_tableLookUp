# STEP 5 of 5:
#
# This last script will go through and delete the newly created ZIP and Unzipped files for
# Clean up. This does not need to be run unless you want to clean the folders up. If you run from
# The beginning again, files will be overwritten automatically with the same name.


import os
import shutil

# Folder paths
output_folder_zip = r'Path to where zipped files are'
output_folder_unzipped = r'Path to where unzipped files are'

# Function to delete all files in a folder
def delete_all_files(folder):
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

# Delete all files in the Out_with_Zip folder
delete_all_files(output_folder_zip)
print(f"All files in {output_folder_zip} deleted.")

# Delete all files in the Unzipped_Files folder
delete_all_files(output_folder_unzipped)
print(f"All files in {output_folder_unzipped} deleted.")
