import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

original_names = []
new_names = []
folder_path = ""

def preview_changes():
    global original_names, new_names, folder_path

    folder_path = filedialog.askdirectory(title="Select Folder")
    if not folder_path:
        return

    pattern = pattern_entry.get().strip()
    if not pattern:
        messagebox.showerror("Error", "Regex pattern cannot be empty.")
        return

    original_names.clear()
    new_names.clear()
    preview_text.delete("1.0", tk.END)

    for filename in os.listdir(folder_path):
        new_name = re.sub(pattern, '', filename).strip()
        if new_name != filename:
            original_names.append(filename)
            new_names.append(new_name)
            preview_text.insert(tk.END, f"{filename} -> {new_name}\n")

    if not original_names:
        preview_text.insert(tk.END, "No files to rename with given pattern.")

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
        if os.path.exists(os.path.join(folder_path, new)):
            os.rename(os.path.join(folder_path, new), os.path.join(folder_path, orig))

    messagebox.showinfo("Reverted", f"Reverted {len(original_names)} file(s).")
    preview_text.insert(tk.END, "\nChanges reverted.\n")

# GUI setup
root = tk.Tk()
root.title("Acolyte File Cleaner (regex removal)")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Regex pattern to remove:").pack(anchor="w")
pattern_entry = tk.Entry(frame, width=50)
pattern_entry.pack()

tk.Button(frame, text="Preview Changes", command=preview_changes).pack(pady=5)
tk.Button(frame, text="Apply Changes", command=apply_changes).pack(pady=5)
tk.Button(frame, text="Revert Changes", command=revert_changes).pack(pady=5)

tk.Label(frame, text="Preview:").pack(anchor="w", pady=(10, 0))
preview_text = scrolledtext.ScrolledText(frame, width=60, height=15)
preview_text.pack()

root.mainloop()
