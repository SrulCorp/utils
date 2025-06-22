import os
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://crawl.chaosforge.org"
ALL_PAGES_URL = f"{BASE_URL}/Special:AllPages"
SAVE_ROOT = "C:\\Users\\Srulik's User\\Downloads\\ytdlp downloads\\Crawl Wiki"
PROGRESS_LOG = os.path.join(SAVE_ROOT, "downloaded_articles.txt")

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name)

def load_downloaded_titles():
    if os.path.exists(PROGRESS_LOG):
        with open(PROGRESS_LOG, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    return set()

def mark_as_downloaded(title):
    with open(PROGRESS_LOG, "a", encoding="utf-8") as f:
        f.write(title + "\n")

def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # Uncomment if you want headless mode
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_all_article_links(driver):
    print("Fetching all article links...")
    links = set()
    driver.get(ALL_PAGES_URL)

    while True:
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_links = soup.select("#mw-content-text ul li a")
        for a in page_links:
            href = a.get("href")
            if href and href.startswith("/wiki/") and not href.startswith("/wiki/Special:"):
                full_url = BASE_URL + href
                links.add(full_url)
        next_link = soup.find("a", text=lambda t: t and t.strip().startswith("Next page"))
        if next_link and next_link.get("href"):
            next_url = BASE_URL + next_link.get("href")
            print(f"Following: {next_url}")
            driver.get(next_url)
        else:
            break

    return sorted(links)

def download_article_selenium(driver, url):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    title_tag = soup.find("h1", id="firstHeading")
    content_tag = soup.find("div", class_="mw-parser-output")
    category_links = soup.select("#mw-normal-catlinks ul li a")

    if not title_tag or not content_tag:
        print(f"Skipping malformed page: {url}")
        return None, None, None

    title = title_tag.text.strip()
    content = content_tag.get_text(separator="\n").strip()
    categories = [cat.text.strip() for cat in category_links]
    return title, content, categories

def save_article(title, content, categories):
    base_filename = sanitize_filename(title) + ".txt"
    if not categories:
        categories = ["Uncategorized"]

    for i, cat in enumerate(categories):
        folder = os.path.join(SAVE_ROOT, sanitize_filename(cat))
        os.makedirs(folder, exist_ok=True)

        suffix = f"_{i}" if i > 0 else ""
        filename = sanitize_filename(title) + suffix + ".txt"
        path = os.path.join(folder, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved '{title}' to '{folder}' as '{filename}'.")

def main():
    driver = get_driver()
    downloaded_titles = load_downloaded_titles()

    try:
        article_links = get_all_article_links(driver)
        print(f"Found {len(article_links)} articles.")

        for idx, url in enumerate(article_links):
            title_guess = url.rsplit("/", 1)[-1].replace("_", " ")

            if title_guess in downloaded_titles:
                print(f"[{idx+1}/{len(article_links)}] Skipping (already saved): {title_guess}")
                continue

            print(f"[{idx+1}/{len(article_links)}] Processing: {url}")
            title, content, categories = download_article_selenium(driver, url)
            if title and content:
                save_article(title, content, categories)
                mark_as_downloaded(title)
            else:
                print(f"Skipping article due to missing data: {url}")
            time.sleep(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
