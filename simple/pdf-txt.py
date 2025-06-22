import os
import pdfminer.high_level

def convert_pdf_to_text(pdf_path, txt_path):
    """Converts a single PDF file to a text file."""
    try:
        text = pdfminer.high_level.extract_text(pdf_path)
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)
        print(f"Converted: {pdf_path} -> {txt_path}")
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")

def process_directory(root_dir):
    """Recursively finds and converts all PDFs in a directory."""
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(foldername, filename)
                txt_path = os.path.splitext(pdf_path)[0] + ".txt"
                convert_pdf_to_text(pdf_path, txt_path)

if __name__ == "__main__":
    input_dir = input("Enter the directory path: ").strip()
    
    if not os.path.isdir(input_dir):
        print("Invalid directory. Please enter a valid path.")
    else:
        process_directory(input_dir)
