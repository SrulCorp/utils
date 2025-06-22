import os
import re
import shutil

# --- Configuration ---
ROOT_DIR = "C:\\Users\\Srulik's User\\Downloads\\ytdlp downloads\\The Coppermind"
MIN_FILES = 10

# --- Logic ---
def is_original(filename):
    """Returns True if filename does NOT end with _#.txt"""
    base = os.path.basename(filename)
    return not re.match(r".+_\d+\.txt$", base)

def clean_categories(root_dir):
    deleted_folders = []

    for category in os.listdir(root_dir):
        category_path = os.path.join(root_dir, category)
        if not os.path.isdir(category_path):
            continue

        files = [f for f in os.listdir(category_path) if f.endswith(".txt")]
        if len(files) >= MIN_FILES:
            continue

        has_original = any(is_original(f) for f in files)

        if not has_original:
            print(f"Deleting: {category_path} (only {len(files)} files, no originals)")
            shutil.rmtree(category_path)
            deleted_folders.append(category)

    print(f"\nDeleted {len(deleted_folders)} folder(s): {deleted_folders}")

# --- Run ---
if __name__ == "__main__":
    clean_categories(ROOT_DIR)
