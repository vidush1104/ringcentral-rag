from typing import List

def split_into_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Very simple chunker based on words or approximate tokens.
    For demo, we can just use word-based splitting.
    Replace with a tokenizer-aware implementation if needed.
    """
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start = end - overlap  # slide with overlap
        if start < 0:
            start = 0

    return chunks
