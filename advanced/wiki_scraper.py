import os
import requests
from bs4 import BeautifulSoup

# Base URL and paths
BASE_URL = "http://crawl.chaosforge.org"
ALL_PAGES_HTML = "all pages.html" # Replace with your local file path
OUTPUT_DIR = "C:\\Users\\Srulik's User\\OneDrive\\Documents\\crawl wiki"

def clean_html(file_path):
    """Extract valid HTML content from a file."""
    with open(file_path, "rb") as file:
        content = file.read()
    html_start = content.find(b"<html")
    return content[html_start:].decode("utf-8", errors="ignore") if html_start != -1 else None

def normalize_url(href):
    """Ensure all URLs are absolute."""
    if href.startswith("/"):
        return f"{BASE_URL}{href}"
    if href.startswith(BASE_URL):
        return href
    return None # Skip invalid or external links

def fetch_and_save_content(url, base_directory):
    """Fetch and save the content of a page, preserving its full directory structure."""
    try:
        # Fetch page content
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            print(f"No content found for {url}")
            return
        text_content = content_div.get_text(separator="\n", strip=True)

        # Extract the full path from the URL
        path_parts = url.replace(BASE_URL, "").strip("/").split("/")
        
        # Recreate the full directory structure
        directory_path = os.path.join(base_directory, *path_parts[:-1])
        os.makedirs(directory_path, exist_ok=True)
        
        # Save the file with the last part of the path as filename
        filename = path_parts[-1] if len(path_parts) > 0 else "index"
        if not filename.endswith(".html"): # Ensure valid extension
            filename += ".txt"
        else:
            filename = filename.replace(".html", ".txt")
        
        filepath = os.path.join(directory_path, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(text_content)
        print(f"Saved: {filepath}")
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

def scrape_all_pages(file_path, output_dir):
    """Scrape all pages listed in the file."""
    cleaned_html = clean_html(file_path)
    if not cleaned_html:
        print("Failed to clean the input file.")
        return
    soup = BeautifulSoup(cleaned_html, "html.parser")
    links = soup.find_all("a", href=True)
    visited = set()
    for link in links:
        href = normalize_url(link["href"])
        if href and href not in visited:
            visited.add(href)
            page_name = href.split("/")[-1]
            fetch_and_save_content(href, output_dir)

if __name__ == "__main__":
    scrape_all_pages(ALL_PAGES_HTML, OUTPUT_DIR)