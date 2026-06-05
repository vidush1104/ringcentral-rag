import argparse
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from rag import answer_question


# ---------- CLI entrypoint ----------

def cli():
    parser = argparse.ArgumentParser(description="RingCentral RAG assistant")
    parser.add_argument("question", type=str, help="User question about RingCentral")
    args = parser.parse_args()

    result = answer_question(args.question)
    print("\n=== Answer ===\n")
    print(result["answer"])
    print("\n=== Sources ===\n")
    for src in result["sources"]:
        print(f"- {src['title']} :: {src['url']} (score={src['score']:.3f})")


# ---------- FastAPI service ----------

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list
    used_fallback: bool


app = FastAPI(title="RingCentral RAG Service")


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    result = answer_question(req.question)
    return AskResponse(**result)


if __name__ == "__main__":
    # If run as script, default to CLI mode.
    # For API: `uvicorn app:app --reload`
    cli()
