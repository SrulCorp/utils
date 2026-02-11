import csv
import os
import time
import requests
from typing import Dict, Optional

SCRYFALL_API_BASE = "https://api.scryfall.com"
REQUEST_DELAY = 0.1  # seconds (Scryfall recommends max 10 requests/sec)

OUTPUT_DIR = r"C:\Users\SrulC\Downloads\MTG Images"  # fixed output folder


def ensure_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def read_csv(path: str):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # strip spaces and surrounding quotes
            yield {k.lower(): v.strip().strip('"') for k, v in row.items() if v}


def fetch_card_by_id(scryfall_id: str) -> Optional[Dict]:
    url = f"{SCRYFALL_API_BASE}/cards/{scryfall_id}"
    r = requests.get(url)
    return r.json() if r.ok else None


def fetch_card_by_oracle_id(oracle_id: str) -> Optional[Dict]:
    url = f"{SCRYFALL_API_BASE}/cards/search"
    params = {"q": f"oracleid:{oracle_id}"}
    r = requests.get(url, params=params)
    if not r.ok:
        return None
    data = r.json()
    return data["data"][0] if data.get("data") else None


def fetch_card_by_name(name: str) -> Optional[Dict]:
    url = f"{SCRYFALL_API_BASE}/cards/named"
    params = {"exact": name}
    r = requests.get(url, params=params)
    return r.json() if r.ok else None


def extract_image_url(card: Dict) -> Optional[str]:
    # Prefer highest quality PNG
    if "image_uris" in card:
        return card["image_uris"].get("png") or card["image_uris"].get("large")

    if "card_faces" in card:
        for face in card["card_faces"]:
            if "image_uris" in face:
                return face["image_uris"].get("png") or face["image_uris"].get("large")

    return None


def sanitize_filename(text: str) -> str:
    return "".join(c for c in text if c.isalnum() or c in (" ", "-", "_")).rstrip()


def download_image(url: str, filepath: str) -> None:
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filepath, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)


def get_unique_filepath(directory: str, filename: str) -> str:
    base, ext = os.path.splitext(filename)
    counter = 1
    candidate = filename

    while os.path.exists(os.path.join(directory, candidate)):
        counter += 1
        candidate = f"{base}_{counter}{ext}"

    return os.path.join(directory, candidate)


def resolve_card(row: Dict) -> Optional[Dict]:
    if "scryfall_id" in row:
        return fetch_card_by_id(row["scryfall_id"])

    if "oracle_id" in row:
        return fetch_card_by_oracle_id(row["oracle_id"])

    if "name" in row:
        return fetch_card_by_name(row["name"])

    return None


def main():
    csv_path = input("Enter path to CSV file: ").strip()
    ensure_directory(OUTPUT_DIR)

    for row in read_csv(csv_path):
        card = resolve_card(row)
        if not card:
            print("Skipping row (card not found):", row)
            continue

        image_url = extract_image_url(card)
        if not image_url:
            print("No image available:", card.get("name"))
            continue

        card_name = sanitize_filename(card.get("name", "unknown"))
        set_code = card.get("set", "unknown")
        collector_number = card.get("collector_number", "0")

        base_filename = f"{card_name}_{set_code}_{collector_number}.jpg"
        filepath = get_unique_filepath(OUTPUT_DIR, base_filename)

        try:
            download_image(image_url, filepath)
            print("Downloaded:", os.path.basename(filepath))
        except Exception as e:
            print("Failed:", os.path.basename(filepath), e)

        time.sleep(REQUEST_DELAY)


if __name__ == "__main__":
    main()
