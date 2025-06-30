import os
import requests
from bs4 import BeautifulSoup

# Base site URL for full link construction
BASE_URL = "https://www.photopea.com/"  # Replace with actual site

# Replace with your raw HTML (li elements block)
HTML_SNIPPET = """<li class="lvl0"><a href="/learn/">Introduction</a></li>
			<li class="lvl0 active"><a href="/learn/workspace">Workspace</a></li>
			<li class="lvl1"><a href="/learn/opening-saving">Open and Save</a></li>
			<li class="lvl1"><a href="/learn/navigation">Navigation</a></li>
			<li class="lvl1"><a href="/learn/image-size">Image size</a></li>
			<li class="lvl0"><a href="/learn/layers">Layers</a></li>
			<li class="lvl1"><a href="/learn/masks">Masks</a></li>
			<li class="lvl1"><a href="/learn/layer-styles">Layer Styles</a></li>
			<li class="lvl1"><a href="/learn/smart-objects">Smart Objects</a></li>
			<li class="lvl1"><a href="/learn/other-layers">Other Layers</a></li>
			<li class="lvl0"><a href="/learn/layer-manipulation">Layer Editing</a></li>
			<li class="lvl1"><a href="/learn/free-transform">Free Transform</a></li>
			<li class="lvl1"><a href="/learn/adjustments-filters">Adjust. &amp; Filters</a></li>
			<li class="lvl0"><a href="/learn/selections">Selections</a></li>
			<li class="lvl1"><a href="/learn/creating-selections">Make Selections</a></li>
			<li class="lvl1"><a href="/learn/advanced-selecting">Advanced Selecting</a></li>
			<li class="lvl1"><a href="/learn/refine-edge">Refine Edge</a></li>
			<li class="lvl1"><a href="/learn/moving-selected-data">Move Selected Data</a></li>
			<li class="lvl0"><a href="/learn/channels">Channels</a></li>
			<li class="lvl0"><a href="/learn/brush-tools">Brush Tools</a></li>
			<li class="lvl1"><a href="/learn/bt-basic">Basic Tools</a></li>
			<li class="lvl1"><a href="/learn/bt-advanced">Advanced Tools</a></li>
			<li class="lvl1"><a href="/learn/bt-smart">Smart Tools</a></li>
			<li class="lvl0"><a href="/learn/text">Text</a></li>
			<li class="lvl1"><a href="/learn/text-style">Text Style</a></li>
			<li class="lvl0"><a href="/learn/vector-graphics">Vector Graphics</a></li>
			<li class="lvl1"><a href="/learn/vg-structure">The Structure</a></li>
			<li class="lvl1"><a href="/learn/vg-manipulation">Editing Shapes</a></li>
			<li class="lvl1"><a href="/learn/vg-creating">Creating Shapes</a></li>
			<li class="lvl1"><a href="/learn/vg-vectorize">Vectorize Bitmap</a></li>
			<li class="lvl0"><a href="/learn/automate">Automate</a></li>
			<li class="lvl1"><a href="/learn/actions">Actions</a></li>
			<li class="lvl1"><a href="/learn/scripts">Scripts</a></li>
			<li class="lvl1"><a href="/learn/variables">Variables</a></li>
			<li class="lvl0"><a href="/learn/other">Other</a></li>
			<li class="lvl1"><a href="/learn/storages">Storages</a></li>
			<li class="lvl1"><a href="/learn/artboards">Artboards</a></li>
			<li class="lvl1"><a href="/learn/color-spaces">Color Spaces</a></li>
			<li class="lvl1"><a href="/learn/guides-grid-snapping">Guides &amp; Snapping</a></li>
			<li class="lvl1"><a href="/learn/animations">Animations</a></li>
			<li class="lvl1"><a href="/learn/slices">Slices</a></li>
			<li class="lvl1"><a href="/learn/vanishing-point">Vanishing Point Filter</a></li>
			<li class="lvl1"><a href="/learn/blur-gallery">Blur Gallery Filter</a></li>
			<li class="lvl1"><a href="/learn/layer-comps">Layer Comps</a></li>
			</ul>
"""

# Output directory for saved text files
OUTPUT_DIR = r"C:\Users\Srulik's User\Downloads\ytdlp downloads\scraped_pages"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Parse links from the HTML snippet
soup = BeautifulSoup(HTML_SNIPPET, 'html.parser')
links = [(a['href'], a.text.strip()) for a in soup.find_all('a', href=True)]

# Scrape each link
for href, title in links:
    full_url = BASE_URL + href
    filename = href.strip("/").replace("/", "_") or "index"
    filepath = os.path.join(OUTPUT_DIR, f"{filename}.txt")

    print(f"Scraping {full_url}...")

    try:
        res = requests.get(full_url)
        res.raise_for_status()

        page_soup = BeautifulSoup(res.text, 'html.parser')

        # Try to extract content - you can refine the tag used here
        main = page_soup.find('main') or page_soup.find('article') or page_soup.body
        text = main.get_text(separator='\n', strip=True) if main else 'No content found.'

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n\n{text}")

        print(f"Saved to {filepath}")

    except Exception as e:
        print(f"Failed to scrape {full_url}: {e}")
