import os
import glob
import re

# Supported audio + video extensions
MEDIA_EXTENSIONS = [
    '*.mp3', '*.wav', '*.flac', '*.aac', '*.ogg', '*.m4a',   # audio
    '*.mp4', '*.mkv', '*.avi', '*.mov', '*.wmv', '*.flv', '*.webm'  # video
]

def prepend_numbers_to_media_files(folder_path, start_number):
    media_files = []

    # Collect all matching files
    for ext in MEDIA_EXTENSIONS:
        media_files.extend(glob.glob(os.path.join(folder_path, ext)))

    # Sort by creation time (change to getmtime for modified time)
    media_files.sort(key=os.path.getctime)

    # Pattern for already-numbered files
    number_pattern = re.compile(r'^\d{3} - ')

    for index, file_path in enumerate(media_files, start=start_number):
        folder, file_name = os.path.split(file_path)

        if number_pattern.match(file_name):
            print(f"Skipping already numbered file: {file_name}")
            continue

        new_file_name = f"{index:03d} - {file_name}"
        new_file_path = os.path.join(folder, new_file_name)

        os.rename(file_path, new_file_path)
        print(f"Renamed '{file_name}' → '{new_file_name}'")

    input("Renaming complete. Press Enter to exit.")


if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")

    while True:
        try:
            start_number = int(input("Enter the starting number (e.g., 1, 2, 3): "))
            if start_number < 0:
                print("Please enter a positive number.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    prepend_numbers_to_media_files(folder_path, start_number)
