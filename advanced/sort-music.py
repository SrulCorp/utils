import os
import shutil
from mutagen import File
from mutagen.easyid3 import EasyID3
import string

# Accepted audio formats
AUDIO_EXTENSIONS = ('.mp3', '.flac', '.m4a', '.aac', '.ogg', '.wav')

def sanitize_filename(name):
    # Remove characters not allowed in filenames
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    return ''.join(c for c in name if c in valid_chars).strip()

def get_audio_metadata(filepath):
    try:
        audio = File(filepath, easy=True)
        if not audio:
            return None

        artist = audio.get('artist', ['Unknown Artist'])[0]
        album = audio.get('album', ['Unknown Album'])[0]
        title = audio.get('title', [os.path.splitext(os.path.basename(filepath))[0]])[0]

        return sanitize_filename(artist), sanitize_filename(album), sanitize_filename(title)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def organize_audio_files(source_dir, destination_dir):
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(AUDIO_EXTENSIONS):
                full_path = os.path.join(root, file)
                metadata = get_audio_metadata(full_path)

                if not metadata:
                    print(f"Skipping (no metadata): {full_path}")
                    continue

                artist, album, title = metadata
                dest_folder = os.path.join(destination_dir, artist, album)
                os.makedirs(dest_folder, exist_ok=True)

                ext = os.path.splitext(file)[1]
                new_filename = f"{title}{ext}"
                dest_path = os.path.join(dest_folder, new_filename)

                counter = 1
                while os.path.exists(dest_path):
                    new_filename = f"{title}_{counter}{ext}"
                    dest_path = os.path.join(dest_folder, new_filename)
                    counter += 1

                shutil.move(full_path, dest_path)
                print(f"Moved: {file} → {dest_path}")

# Example usage
source_directory = r"F:\Music"
destination_directory = r"F:\Sorted"

organize_audio_files(source_directory, destination_directory)
