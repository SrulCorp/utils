import os
import glob
import re

def prepend_numbers_to_audio_files(folder_path, start_number):
    # Get all audio files in the folder
    audio_files = glob.glob(os.path.join(folder_path, '*.mp3')) + \
                  glob.glob(os.path.join(folder_path, '*.wav')) + \
                  glob.glob(os.path.join(folder_path, '*.flac')) + \
                  glob.glob(os.path.join(folder_path, '*.aac')) + \
                  glob.glob(os.path.join(folder_path, '*.ogg')) + \
                  glob.glob(os.path.join(folder_path, '*.m4a'))

    # Sort files by creation time
    audio_files.sort(key=os.path.getctime)

    # Prepend numbers to file names, ignoring files already numbered
    number_pattern = re.compile(r'^\d{3} - ')
    for index, file_path in enumerate(audio_files, start=start_number):
        folder, file_name = os.path.split(file_path)
        if number_pattern.match(file_name):
            print(f"Skipping already numbered file: {file_name}")
            continue
        new_file_name = f"{index:03d} - {file_name}"
        new_file_path = os.path.join(folder, new_file_name)
        os.rename(file_path, new_file_path)
        print(f"Renamed '{file_name}' to '{new_file_name}'")

    input("Renaming complete. Press Enter to exit.")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")

    # Validate the start number
    while True:
        try:
            start_number = int(input("Enter the starting number (e.g., 001, 002, ...): "))
            if start_number < 0:
                print("Please enter a positive number.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    prepend_numbers_to_audio_files(folder_path, start_number)

# import os
# import re
# import glob
# import tkinter as tk
# from tkinter import filedialog, messagebox, scrolledtext
# 
# original_names = []
# new_names = []
# folder_path = ""
# 
# def get_audio_files(path):
#     audio_files = []
#     for ext in ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a']:
#         audio_files.extend(glob.glob(os.path.join(path, f'*.{ext}')))
#         audio_files.extend(glob.glob(os.path.join(path, f'*.{ext.upper()}')))
#     return sorted(audio_files, key=os.path.getctime)
# 
# def preview_changes():
#     global original_names, new_names, folder_path
# 
#     folder_path = filedialog.askdirectory(title="Select Folder")
#     if not folder_path:
#         return
# 
#     try:
#         start_number = int(start_entry.get().strip())
#         if start_number < 0:
#             raise ValueError
#     except ValueError:
#         messagebox.showerror("Error", "Please enter a valid positive starting number.")
#         return
# 
#     original_names.clear()
#     new_names.clear()
#     preview_text.delete("1.0", tk.END)
# 
#     number_pattern = re.compile(r'^\d{3} - ')
#     audio_files = get_audio_files(folder_path)
# 
#     for idx, file_path in enumerate(audio_files, start=start_number):
#         folder, file_name = os.path.split(file_path)
#         if number_pattern.match(file_name):
#             continue
#         new_file_name = f"{idx:03d} - {file_name}"
#         original_names.append(file_name)
#         new_names.append(new_file_name)
#         preview_text.insert(tk.END, f"{file_name} -> {new_file_name}\n")
# 
#     if not original_names:
#         preview_text.insert(tk.END, "No files to rename (all may already be numbered).")
# 
# def apply_changes():
#     if not original_names:
#         messagebox.showwarning("Warning", "No changes to apply.")
#         return
# 
#     for orig, new in zip(original_names, new_names):
#         try:
#             os.rename(os.path.join(folder_path, orig), os.path.join(folder_path, new))
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to rename {orig}: {e}")
#             return
# 
#     messagebox.showinfo("Success", f"Renamed {len(original_names)} file(s).")
#     preview_text.insert(tk.END, "\nChanges applied.\n")
# 
# def revert_changes():
#     if not original_names:
#         messagebox.showwarning("Warning", "Nothing to revert.")
#         return
# 
#     for orig, new in zip(original_names, new_names):
#         orig_path = os.path.join(folder_path, orig)
#         new_path = os.path.join(folder_path, new)
#         if os.path.exists(new_path):
#             os.rename(new_path, orig_path)
# 
#     messagebox.showinfo("Reverted", f"Reverted {len(original_names)} file(s).")
#     preview_text.insert(tk.END, "\nChanges reverted.\n")
# 
# # GUI setup
# root = tk.Tk()
# root.title("Acolyte Audio File Renamer (Sequential Numbering)")
# 
# frame = tk.Frame(root, padx=20, pady=20)
# frame.pack()
# 
# tk.Label(frame, text="Starting Number:").pack(anchor="w")
# start_entry = tk.Entry(frame, width=10)
# start_entry.insert(0, "1")
# start_entry.pack(anchor="w", pady=(0, 10))
# 
# tk.Button(frame, text="Preview Changes", command=preview_changes).pack(pady=5)
# tk.Button(frame, text="Apply Changes", command=apply_changes).pack(pady=5)
# tk.Button(frame, text="Revert Changes", command=revert_changes).pack(pady=5)
# 
# tk.Label(frame, text="Preview:").pack(anchor="w", pady=(10, 0))
# preview_text = scrolledtext.ScrolledText(frame, width=60, height=15)
# preview_text.pack()
# 
# root.mainloop()
# 