from typing import List, Dict

import chromadb
from chromadb.config import Settings

from config import (
    VECTOR_STORE_DIR,
    VECTOR_COLLECTION_NAME,
    TOP_K,
    SIMILARITY_THRESHOLD,
    FALLBACK_MESSAGE,
    LLM_MODEL_NAME,
)
from llm import generate_answer  # you will define this


def get_collection():
    client = chromadb.PersistentClient(
        path=VECTOR_STORE_DIR,
        settings=Settings(anonymized_telemetry=False),
    )
    return client.get_collection(name=VECTOR_COLLECTION_NAME)


def retrieve_context(question: str) -> Dict:
    """
    Retrieve top-k relevant chunks for a question from the vector store.
    Returns dict with 'hits' (list of {text, url, title, score}).
    """
    collection = get_collection()
    results = collection.query(
        query_texts=[question],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc, meta, dist in zip(docs, metas, distances):
        score = 1 - dist  # if using cosine distance; adjust if different
        hits.append(
            {
                "text": doc,
                "url": meta.get("url"),
                "title": meta.get("title"),
                "score": score,
            }
        )

    return {"hits": hits}


def answer_question(question: str) -> Dict:
    """
    High-level RAG pipeline:
    1) retrieve context
    2) decide if we have enough signal
    3) if yes, call LLM with strict prompt and context
    4) if no, return fallback
    """
    retrieval = retrieve_context(question)
    hits = retrieval["hits"]

    if not hits:
        return {"answer": FALLBACK_MESSAGE, "sources": [], "used_fallback": True}

    best_score = max(h["score"] for h in hits)
    if best_score < SIMILARITY_THRESHOLD:
        return {"answer": FALLBACK_MESSAGE, "sources": [], "used_fallback": True}

    context_blocks = []
    for h in hits:
        context_blocks.append(f"Source URL: {h['url']}\nTitle: {h['title']}\nText:\n{h['text']}\n")

    full_context = "\n\n---\n\n".join(context_blocks)

    system_prompt = (
        "You are a RingCentral documentation assistant.\n"
        "You must answer ONLY using the provided context, which comes from "
        "RingCentral’s public website.\n"
        "If the answer is not clearly supported by the context, respond with:\n"
        f"\"{FALLBACK_MESSAGE}\"\n"
        "Never invent prices, contract terms, or guarantees.\n"
        "Include relevant RingCentral URLs in your answer when helpful.\n"
    )

    answer = generate_answer(
        model_name=LLM_MODEL_NAME,
        system_prompt=system_prompt,
        context=full_context,
        question=question,
    )

    sources = [
        {"url": h["url"], "title": h["title"], "score": h["score"]} for h in hits
    ]

    return {"answer": answer, "sources": sources, "used_fallback": False}
