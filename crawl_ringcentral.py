import json
import time
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

from config import (
    RINGCENTRAL_SITEMAP_URL,
    RINGCENTRAL_BASE_URL,
    CRAWL_TIMEOUT,
    CRAWL_SLEEP_SECONDS,
    MAX_PAGES,
)
from utils.html_cleaner import extract_main_content


def fetch_sitemap_urls() -> List[str]:
    """
    Fetch the RingCentral sitemap HTML and extract internal links
    under the base domain. This is a simple HTML sitemap parser.[web:15]
    """
    resp = requests.get(RINGCENTRAL_SITEMAP_URL, timeout=CRAWL_TIMEOUT)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    urls = set()

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("/"):
            href = RINGCENTRAL_BASE_URL + href
        if href.startswith(RINGCENTRAL_BASE_URL):
            urls.add(href)

    # Optionally: filter to only certain paths (products, solutions, pricing, etc.)
    # urls = {u for u in urls if "plansandpricing" in u or "/solutions/" in u}

    return list(urls)[:MAX_PAGES]


def fetch_page(url: str) -> Dict:
    """
    Fetch a single page and return its structured content.
    """
    resp = requests.get(url, timeout=CRAWL_TIMEOUT)
    resp.raise_for_status()

    content = extract_main_content(resp.text)
    content["url"] = url
    return content


def crawl_ringcentral() -> List[Dict]:
    """
    Crawl a subset of RingCentral pages and return a list of {url, title, text}.
    """
    urls = fetch_sitemap_urls()
    pages: List[Dict] = []

    for i, url in enumerate(urls, start=1):
        try:
            print(f"[{i}/{len(urls)}] Fetching {url}")
            page = fetch_page(url)
            pages.append(page)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        time.sleep(CRAWL_SLEEP_SECONDS)

    return pages


def main():
    pages = crawl_ringcentral()
    output_path = "data/ringcentral_pages.json"
    print(f"Saving {len(pages)} pages to {output_path}")
    # Ensure data dir exists
    import os
    os.makedirs("data", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
