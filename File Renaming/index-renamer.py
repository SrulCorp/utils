import os

def rename_index_files(root_dir: str) -> None:
    for current_dir, _, files in os.walk(root_dir):
        if "index.html" in files:
            parent_folder = os.path.basename(current_dir)
            old_path = os.path.join(current_dir, "index.html")

            new_filename = f"z - {parent_folder}.html"
            new_path = os.path.join(current_dir, new_filename)

            if os.path.exists(new_path):
                print(f"SKIPPED (already exists): {new_path}")
                continue

            os.rename(old_path, new_path)
            print(f"RENAMED: {old_path} -> {new_path}")

if __name__ == "__main__":
    root_directory = input("Enter the root directory to process: ").strip()

    if not os.path.isdir(root_directory):
        print("ERROR: Provided path is not a valid directory.")
    else:
        rename_index_files(root_directory)
