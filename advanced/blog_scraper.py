import os
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.brandonsanderson.com'
BLOG_URL = f'{BASE_URL}/blogs/blog'
OUTPUT_DIR = r"C:\Users\Srulik's User\Downloads\ytdlp downloads\sanderson_blog_posts"

# Create the output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get blog post links from a single page
def get_blog_posts(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.select('div.blog-item__title-holder a')
    return [BASE_URL + post['href'] for post in posts]

# Extract the title, date, and content of a post
def get_post_content(post_url):
    response = requests.get(post_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract slug from URL to use as fallback title
    url_slug = post_url.rstrip('/').split('/')[-1]

    # Get the title or fallback to URL slug
    title_tag = soup.find('h1', class_='h2')
    title = title_tag.get_text(strip=True) if title_tag else url_slug or "Untitled"

    # Get the date
    date_tag = soup.find('div', class_='blog-item__date')
    date = date_tag.get_text(strip=True) if date_tag else "No Date"

    # Find the main article content
    article = soup.find('article')
    if not article:
        return title, f"{title}\n{date}\n\nNo content found."

    # Collect paragraphs and headers inside article
    content_parts = []
    for tag in article.find_all(['p', 'div', 'h2', 'h3', 'li']):
        text = tag.get_text(strip=True)
        if text and not text.startswith("Share"):
            content_parts.append(text)

    content = '\n\n'.join(content_parts).strip() or "No content found."
    return title, f"{title}\n{date}\n\n{content}"



# Save post content to a text file
def save_post(title, content, index):
    # Sanitize title
    base = title or "Untitled"
    safe_title = ''.join(c if c.isalnum() or c == ' ' else '_' for c in base).strip()
    safe_title = '_'.join(safe_title.split())[:40]  # short and clean
    safe_title = safe_title or "Untitled"

    # Format filename with index
    filename = f"{index:03d} - {safe_title}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


# Main scraping loop
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    index = 1  # for filename numbering

    for page_number in range(1, 276):  # Adjust max if needed
        print(f"Scraping page {page_number}...")
        page_url = f'{BLOG_URL}?page={page_number}'
        post_urls = get_blog_posts(page_url)

        if not post_urls:
            print("No more posts found.")
            break

        for post_url in post_urls:
            try:
                print(f"  Fetching post: {post_url}")
                title, content = get_post_content(post_url)
                save_post(title, content, index)
                index += 1
                time.sleep(1)  # Be polite to the server
            except Exception as e:
                print(f"  Failed to process {post_url}: {e}")

        time.sleep(2)


if __name__ == '__main__':
    main()
