from typing import List
# Plug in your provider of choice: OpenAI, Gemini, or sentence-transformers

from config import OPENAI_API_KEY


def embed_texts(texts: List[str], model_name: str) -> List[List[float]]:
    """
    Compute embeddings for a list of texts.
    Replace this with your preferred embedding provider.
    """
    # Pseudocode example with OpenAI:
    # from openai import OpenAI
    # client = OpenAI(api_key=OPENAI_API_KEY)
    #
    # resp = client.embeddings.create(model=model_name, input=texts)
    # return [item.embedding for item in resp.data]
    raise NotImplementedError("Implement embed_texts with your chosen provider.")
