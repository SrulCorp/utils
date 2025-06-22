import os
import re
import glob
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

original_names = []
new_names = []
folder_path = ""

# Supported audio formats
audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']

# GUI logic
def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory(title="Select Folder")
    folder_label.config(text=f"Folder: {folder_path if folder_path else 'None'}")

def preview_changes():
    global original_names, new_names
    original_names.clear()
    new_names.clear()
    preview_text.delete("1.0", tk.END)

    if not folder_path:
        messagebox.showerror("Error", "Please select a folder first.")
        return

    mode = mode_var.get()

    if mode == "regex":
        pattern = pattern_entry.get().strip()
        if not pattern:
            messagebox.showerror("Error", "Regex pattern cannot be empty.")
            return

        for filename in os.listdir(folder_path):
            new_name = re.sub(pattern, '', filename).strip()
            if new_name != filename:
                original_names.append(filename)
                new_names.append(new_name)
                preview_text.insert(tk.END, f"{filename} -> {new_name}\n")

    elif mode == "number":
        try:
            start_number = int(number_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid starting number.")
            return

        audio_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in audio_extensions]
        audio_files.sort(key=lambda f: os.path.getctime(os.path.join(folder_path, f)))

        number_pattern = re.compile(r'^\d{3} - ')
        for i, file_name in enumerate(audio_files, start=start_number):
            if number_pattern.match(file_name):
                continue
            new_name = f"{i:03d} - {file_name}"
            original_names.append(file_name)
            new_names.append(new_name)
            preview_text.insert(tk.END, f"{file_name} -> {new_name}\n")

    if not original_names:
        preview_text.insert(tk.END, "No files to rename.")

def apply_changes():
    if not original_names:
        messagebox.showwarning("Warning", "No changes to apply.")
        return

    for orig, new in zip(original_names, new_names):
        os.rename(os.path.join(folder_path, orig), os.path.join(folder_path, new))

    messagebox.showinfo("Success", f"Renamed {len(original_names)} file(s).")
    preview_text.insert(tk.END, "\nChanges applied.\n")


def revert_changes():
    if not original_names:
        messagebox.showwarning("Warning", "Nothing to revert.")
        return

    for orig, new in zip(original_names, new_names):
        new_path = os.path.join(folder_path, new)
        if os.path.exists(new_path):
            os.rename(new_path, os.path.join(folder_path, orig))

    messagebox.showinfo("Reverted", f"Reverted {len(original_names)} file(s).")
    preview_text.insert(tk.END, "\nChanges reverted.\n")

def update_mode():
    if mode_var.get() == "regex":
        regex_frame.pack(fill="x", pady=(10, 0))
        number_frame.forget()
    else:
        number_frame.pack(fill="x", pady=(10, 0))
        regex_frame.forget()

# GUI setup
root = tk.Tk()
root.title("Acolyte File Renamer")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

mode_var = tk.StringVar(value="regex")
tk.Label(frame, text="Select Mode:").pack(anchor="w")
tk.Radiobutton(frame, text="Regex Removal", variable=mode_var, value="regex", command=update_mode).pack(anchor="w")
tk.Radiobutton(frame, text="Number Audio Files", variable=mode_var, value="number", command=update_mode).pack(anchor="w")

regex_frame = tk.Frame(frame)
tk.Label(regex_frame, text="Regex pattern to remove:").pack(anchor="w")
pattern_entry = tk.Entry(regex_frame, width=50)
pattern_entry.pack()

number_frame = tk.Frame(frame)
tk.Label(number_frame, text="Starting number:").pack(anchor="w")
number_entry = tk.Entry(number_frame, width=10)
number_entry.insert(0, "1")
number_entry.pack()

regex_frame.pack(fill="x", pady=(10, 0))  # Show regex frame by default

folder_label = tk.Label(frame, text="Folder: None")
folder_label.pack(pady=(10, 0))
tk.Button(frame, text="Select Folder", command=select_folder).pack(pady=5)

btn_frame = tk.Frame(frame)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Preview Changes", command=preview_changes).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Apply Changes", command=apply_changes).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Revert Changes", command=revert_changes).grid(row=0, column=2, padx=5)

preview_text = scrolledtext.ScrolledText(frame, width=70, height=15)
preview_text.pack(pady=(10, 0))

root.mainloop()
