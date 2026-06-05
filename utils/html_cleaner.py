from bs4 import BeautifulSoup

def extract_main_content(html: str) -> dict:
    """
    Extract a reasonable approximation of the main content from a RingCentral HTML page.
    Returns a dict with title and text. This is intentionally simple for demo purposes.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Title
    title_el = soup.find("title")
    title = title_el.get_text(strip=True) if title_el else ""

    # Remove common non-content elements (nav, footer, etc.) - tweak as needed
    for selector in ["header", "footer", "nav", "script", "style"]:
        for tag in soup.find_all(selector):
            tag.decompose()

    # You can add RingCentral-specific class/id filters here once you inspect a few pages.

    # Main text: join visible text from body
    body = soup.find("body")
    if not body:
        text = soup.get_text(separator="\n", strip=True)
    else:
        text = body.get_text(separator="\n", strip=True)

    return {"title": title, "text": text}
