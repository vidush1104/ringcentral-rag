from typing import Optional

from config import OPENAI_API_KEY


def generate_answer(
    model_name: str,
    system_prompt: str,
    context: str,
    question: str,
    temperature: float = 0.2,
    max_tokens: int = 512,
) -> str:
    """
    Call your preferred LLM with a strict system prompt + context + question.
    This is where you plug OpenAI, Gemini, etc.
    """
    # Pseudocode (OpenAI-style):
    #
    # from openai import OpenAI
    # client = OpenAI(api_key=OPENAI_API_KEY)
    #
    # messages = [
    #   {"role": "system", "content": system_prompt},
    #   {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    # ]
    #
    # resp = client.chat.completions.create(
    #   model=model_name,
    #   messages=messages,
    #   temperature=temperature,
    #   max_tokens=max_tokens,
    # )
    # return resp.choices[0].message.content.strip()
    raise NotImplementedError("Implement generate_answer with your chosen provider.")
