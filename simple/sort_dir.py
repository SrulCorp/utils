import os
import shutil

def organize_files_by_letter(directory):
    # Create a folder for subfolders
    folders_path = os.path.join(directory, "folders")
    os.makedirs(folders_path, exist_ok=True)
    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        if os.path.isdir(item_path):
            # Move subfolders to "folders" directory
            if item != "folders":
                shutil.move(item_path, os.path.join(folders_path, item))
        elif os.path.isfile(item_path):
            # Get the first letter of the file's name
            first_letter = item[0].upper()
            if first_letter.isalpha():
                letter_folder = os.path.join(directory, first_letter)
            else:
                letter_folder = os.path.join(directory, "Other")
            
            # Create the letter folder if it doesn't exist
            os.makedirs(letter_folder, exist_ok=True)
            
            # Move the file to the appropriate letter folder
            shutil.move(item_path, os.path.join(letter_folder, item))

# Prompt the user for the directory path
directory_path = input("Enter the directory path to organize: ").strip()

# Check if the provided path is valid
if os.path.isdir(directory_path):
    organize_files_by_letter(directory_path)
    print(f"Files in '{directory_path}' have been organized.")
else:
    print("The provided path is not a valid directory.")
