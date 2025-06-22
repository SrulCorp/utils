import os
import shutil

def sort_folders_by_letter(source_dir, sorted_dir='sorted'):
    # Create the sorted directory if it doesn't exist
    sorted_path = os.path.join(source_dir, sorted_dir)
    os.makedirs(sorted_path, exist_ok=True)

    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)

        # Skip if it's not a folder or if it's the sorted output folder
        if not os.path.isdir(item_path) or item == sorted_dir:
            continue

        first_letter = item[0].lower()
        target_folder = os.path.join(sorted_path, first_letter)
        os.makedirs(target_folder, exist_ok=True)

        # Move the folder into the appropriate letter folder
        shutil.move(item_path, os.path.join(target_folder, item))

    print(f"Folders sorted into '{sorted_dir}' folder by first letter.")

# Example usage
# Replace '/path/to/your/directory' with the actual path
sort_folders_by_letter("C:\\Users\\Srulik's User\\Downloads\\ytdlp downloads\\The Coppermind")
