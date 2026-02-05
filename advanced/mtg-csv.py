import csv
import time
import logging
import requests
from typing import Dict, Optional

SCRYFALL_API_BASE = "https://api.scryfall.com"
REQUEST_DELAY = 0.1  # seconds (max 10 req/sec per Scryfall)

# ---------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def read_csv(path: str):
    logger.info("Reading input CSV: %s", path)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized = {
                k.lower(): v.strip().strip('"')
                for k, v in row.items()
                if v
            }
            logger.debug("Parsed CSV row: %s", normalized)
            yield normalized


def fetch_card_by_id(scryfall_id: str) -> Optional[Dict]:
    logger.debug("Fetching card by Scryfall ID: %s", scryfall_id)
    r = requests.get(f"{SCRYFALL_API_BASE}/cards/{scryfall_id}")
    if not r.ok:
        logger.warning(
            "Failed to fetch card by Scryfall ID %s (HTTP %s)",
            scryfall_id,
            r.status_code,
        )
        return None
    return r.json()


def fetch_card_by_oracle_id(oracle_id: str) -> Optional[Dict]:
    logger.debug("Fetching card by Oracle ID: %s", oracle_id)
    r = requests.get(
        f"{SCRYFALL_API_BASE}/cards/search",
        params={"q": f"oracleid:{oracle_id}"},
    )
    if not r.ok:
        logger.warning(
            "Failed to fetch card by Oracle ID %s (HTTP %s)",
            oracle_id,
            r.status_code,
        )
        return None

    data = r.json()
    if not data.get("data"):
        logger.info("No cards found for Oracle ID: %s", oracle_id)
        return None

    return data["data"][0]


def fetch_card_by_name(name: str) -> Optional[Dict]:
    logger.debug("Fetching card by exact name: %s", name)
    r = requests.get(
        f"{SCRYFALL_API_BASE}/cards/named",
        params={"exact": name},
    )
    if not r.ok:
        logger.warning(
            "Failed to fetch card by name '%s' (HTTP %s)",
            name,
            r.status_code,
        )
        return None
    return r.json()


def extract_png_url(card: Dict) -> Optional[str]:
    if "image_uris" in card:
        return card["image_uris"].get("png")

    if "card_faces" in card:
        for face in card["card_faces"]:
            if "image_uris" in face:
                return face["image_uris"].get("png")

    logger.info(
        "No PNG image found for card: %s",
        card.get("name", "<unknown>"),
    )
    return None


def resolve_card(row: Dict) -> Optional[Dict]:
    if "scryfall_id" in row:
        return fetch_card_by_id(row["scryfall_id"])

    if "oracle_id" in row:
        return fetch_card_by_oracle_id(row["oracle_id"])

    if "name" in row:
        return fetch_card_by_name(row["name"])

    logger.warning("Row does not contain a resolvable identifier: %s", row)
    return None


def main():
    input_csv = input("Enter path to input CSV: ").strip()
    output_csv = input("Enter path to output CSV: ").strip()

    logger.info("Starting processing")
    logger.info("Input CSV: %s", input_csv)
    logger.info("Output CSV: %s", output_csv)

    processed = 0
    written = 0

    with open(output_csv, "w", newline="", encoding="utf-8") as out_f:
        writer = csv.writer(out_f)

        for row in read_csv(input_csv):
            processed += 1
            card = resolve_card(row)
            if not card:
                logger.debug("Skipping row %d: card not resolved", processed)
                continue

            png_url = extract_png_url(card)
            if not png_url:
                logger.debug(
                    "Skipping row %d: no PNG URL available", processed
                )
                continue

            writer.writerow([png_url])
            written += 1
            logger.debug(
                "Wrote PNG URL for card: %s",
                card.get("name", "<unknown>"),
            )

            time.sleep(REQUEST_DELAY)

    logger.info(
        "Processing complete. Rows processed: %d, PNG URLs written: %d",
        processed,
        written,
    )


if __name__ == "__main__":
    main()
