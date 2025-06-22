import os
import re
import requests
from bs4 import BeautifulSoup
import ast

def ask_url_input_mode():
    while True:
        choice = input("Would you like to:\n1. Enter URLs one by one\n2. Paste a list of URLs (Python-style array)\nChoose 1 or 2: ").strip()
        if choice == '1':
            return 'manual'
        elif choice == '2':
            return 'array'
        else:
            print("Invalid input. Please enter 1 or 2.")

def get_urls_from_manual():
    urls = []
    while True:
        url = input("Enter a URL: ").strip()
        if url:
            urls.append(url)
        cont = input("Would you like to add another URL? (y/n): ").strip().lower()
        if cont != 'y':
            break
    return urls

def get_urls_from_array():
    while True:
        array_input = input("Paste the Python-style list of URLs (e.g. [\"https://example.com\", \"https://openai.com\"]):\n").strip()
        try:
            urls = ast.literal_eval(array_input)
            if isinstance(urls, list) and all(isinstance(u, str) for u in urls):
                return urls
            else:
                print("That wasn't a valid list of URLs. Try again.")
        except Exception as e:
            print(f"Error: {e}. Try again.")

def get_directory():
    while True:
        directory = input("Enter the directory where text files should be saved: ").strip()
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Directory '{directory}' created.")
            except Exception as e:
                print(f"Could not create directory: {e}")
                continue
        elif not os.path.isdir(directory):
            print("That path is not a directory. Try again.")
            continue
        return directory

def clean_filename(title):
    # Remove invalid filename characters and truncate if too long
    title = re.sub(r'[\\/*?:"<>|]', '', title)
    return title.strip()[:100] or "untitled"

def fetch_and_save(urls, directory):
    used_filenames = set()

    for url in urls:
        try:
            print(f"Fetching: {url}")
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()

            title_tag = soup.title.string if soup.title and soup.title.string else "untitled"
            filename_base = clean_filename(title_tag)

            filename = filename_base + ".txt"
            count = 1
            while filename in used_filenames or os.path.exists(os.path.join(directory, filename)):
                filename = f"{filename_base}_{count}.txt"
                count += 1
            used_filenames.add(filename)

            filepath = os.path.join(directory, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Saved text to {filepath}")

        except Exception as e:
            print(f"Error processing {url}: {e}")

def main():
    mode = ask_url_input_mode()
    urls = get_urls_from_manual() if mode == 'manual' else get_urls_from_array()

    if not urls:
        print("No URLs provided. Exiting.")
        return

    save_dir = get_directory()
    fetch_and_save(urls, save_dir)

if __name__ == "__main__":
    main()
