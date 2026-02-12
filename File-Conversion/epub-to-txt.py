# DEPENDANCY: BeautifulSoup, ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def epub_to_txt(epub_path, txt_path):
    book = epub.read_epub(epub_path)
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for item in book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                txt_file.write(soup.get_text())

# Example usage
epub_path = "C:/Users/Srulik's User/Downloads/Icarus+Needle+The+Icarus+Series+Book+5+The+-+Timothy+Zahn (1).epub"
txt_path = 'D:/books/Icarus Needle.txt'
epub_to_txt(epub_path, txt_path)
