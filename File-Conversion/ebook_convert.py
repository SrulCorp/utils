import os
from ebooklib import epub
from bs4 import BeautifulSoup
import ebooklib


def convert_epub_to_text(epub_path, output_path):
    try:
        book = epub.read_epub(epub_path)
        text_content = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text_content.append(soup.get_text())
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(text_content))
        print(f"Converted: {epub_path} -> {output_path}")
    except Exception as e:
        print(f"Failed to convert {epub_path}: {e}")


def find_and_convert_epubs(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.epub'):
                epub_path = os.path.join(root, file)
                txt_path = os.path.splitext(epub_path)[0] + '.txt'
                convert_epub_to_text(epub_path, txt_path)


if __name__ == '__main__':
    directory = input("Enter the directory to search for .epub files: ")
    find_and_convert_epubs(directory)
    