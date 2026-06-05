import json
import os
from typing import List, Dict

import chromadb  # or faiss
from chromadb.config import Settings

from config import (
    VECTOR_STORE_DIR,
    VECTOR_COLLECTION_NAME,
    CHUNK_SIZE_TOKENS,
    CHUNK_OVERLAP_TOKENS,
    EMBEDDING_MODEL_NAME,
)
from embeddings import embed_texts  # you will define this
from tokenization import split_into_chunks  # you will define this


def load_pages(path: str = "data/ringcentral_pages.json") -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_vector_store(pages: List[Dict]):
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

    client = chromadb.PersistentClient(
        path=VECTOR_STORE_DIR,
        settings=Settings(anonymized_telemetry=False),
    )
    collection = client.get_or_create_collection(name=VECTOR_COLLECTION_NAME)

    ids: List[str] = []
    documents: List[str] = []
    metadatas: List[Dict] = []

    for page_idx, page in enumerate(pages):
        url = page["url"]
        title = page.get("title", "")
        text = page.get("text", "")

        chunks = split_into_chunks(text, CHUNK_SIZE_TOKENS, CHUNK_OVERLAP_TOKENS)
        for chunk_idx, chunk in enumerate(chunks):
            doc_id = f"{page_idx}-{chunk_idx}"
            ids.append(doc_id)
            documents.append(chunk)
            metadatas.append({"url": url, "title": title, "chunk_idx": chunk_idx})

    # Compute embeddings
    vectors = embed_texts(documents, model_name=EMBEDDING_MODEL_NAME)

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=vectors,
    )


def main():
    pages = load_pages()
    build_vector_store(pages)
    print("Vector store built.")


if __name__ == "__main__":
    main()
