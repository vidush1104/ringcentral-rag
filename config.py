import os
from dotenv import load_dotenv

load_dotenv()

# Core site configuration
RINGCENTRAL_BASE_URL = "https://www.ringcentral.com"
RINGCENTRAL_SITEMAP_URL = f"{RINGCENTRAL_BASE_URL}/sitemap.html"  # static seed page[web:15]

# Crawling
CRAWL_TIMEOUT = 10
CRAWL_SLEEP_SECONDS = 1.0  # be polite to the site
MAX_PAGES = 200  # cap for demo; adjust as needed

# Chunking
CHUNK_SIZE_TOKENS = 512
CHUNK_OVERLAP_TOKENS = 128

# Vector store
VECTOR_STORE_DIR = "index"
VECTOR_COLLECTION_NAME = "ringcentral_pages"

# Embeddings / LLM
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-3-small")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4.1-mini")  # or Gemini, etc.

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # or other provider key
# Add other provider keys here if needed

# Retrieval / QA
TOP_K = 8
SIMILARITY_THRESHOLD = 0.5  # tune empirically

# Fallback message
FALLBACK_MESSAGE = (
    "This information is not clearly documented on RingCentral’s public website. "
    "Please contact the company’s support team for the most accurate details."
)
