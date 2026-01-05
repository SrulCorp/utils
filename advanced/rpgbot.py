import os
import time
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.microsoft import EdgeChromiumDriverManager

BASE_URL = "https://rpgbot.net/dnd5/"
SAVE_ROOT = r"C:\Users\SrulC\Downloads\YTDLP Downloads\RPGbot"

visited = set()
downloaded = set()

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def get_driver():
    options = EdgeOptions()
    options.add_argument("--start-maximized")
    # Uncomment this if you want headless mode:
    # options.add_argument("--headless")
    # Add user-agent to mimic normal browser
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114 Safari/537.36")

    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    return driver

def is_valid_article_url(url):
    return url.startswith(BASE_URL) and not any(x in url for x in ["#", ".pdf", ".jpg", ".png", ".svg"])

def save_article(url, title, content):
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")

    # Fix homepage saving path
    if url.rstrip("/") == BASE_URL.rstrip("/"):
        subfolder = os.path.join(SAVE_ROOT, "home")
        filename = "index.txt"
    else:
        if len(path_parts) > 1:
            subfolder = os.path.join(SAVE_ROOT, *path_parts[:-1])
        else:
            subfolder = os.path.join(SAVE_ROOT, "index")
        filename = sanitize_filename(path_parts[-1] if path_parts[-1] else "index") + ".txt"

    os.makedirs(subfolder, exist_ok=True)
    full_path = os.path.join(subfolder, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"{title}\n\n{content}")

    print(f"Saved: {full_path}")

def scrape_page(driver, url):
    if url in visited:
        return
    visited.add(url)
    print(f"Scraping: {url}")

    try:
        driver.get(url)

        # Wait for main or article tag to load (dynamic content)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
        except:
            print(f"Timeout waiting for main content on {url}")

        soup = BeautifulSoup(driver.page_source, "html.parser")

        title_tag = soup.find("h1")
        content_tag = soup.find("main") or soup.find("article")

        if title_tag and content_tag:
            title = title_tag.get_text().strip()
            content = content_tag.get_text(separator="\n").strip()
            save_article(url, title, content)
            downloaded.add(url)
        else:
            print(f"Missing title or content on: {url}")

        # Crawl internal links recursively
        for a in soup.find_all("a", href=True):
            href = a["href"]
            next_url = urljoin(url, href)
            if is_valid_article_url(next_url) and next_url not in visited:
                scrape_page(driver, next_url)

    except Exception as e:
        print(f"Error scraping {url}: {e}")

def main():
    driver = get_driver()
    try:
        scrape_page(driver, BASE_URL)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
