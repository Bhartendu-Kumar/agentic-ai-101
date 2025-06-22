#!/usr/bin/env python3
"""
demo_search_llm.py
--------------------------------
1. Fetch fresh context with Tavily Search
2. Feed that context to Gemma 3 (1 B) running in Ollama
No built-in tool calls required.
"""
import os
import requests
from textwrap import shorten

# ----------------------------------------------------------------------
# 1) Search helper
# ----------------------------------------------------------------------
def web_search(query: str, max_results: int = 5) -> str:
    """
    Call the Tavily Search API and return concatenated snippets.
    Set TAVILY_API_KEY in your shell before running.
    """
    api_key = "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"
    if not api_key:
        raise RuntimeError("Please set TAVILY_API_KEY first!")

    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": max_results,
        "search_depth": "advanced",
    }
    resp = requests.post("https://api.tavily.com/search", json=payload, timeout=30)
    resp.raise_for_status()

    results = resp.json()["results"]
    snippets = "\n".join(
        f"{item['title']}\n{shorten(item['content'], 250)}"
        for item in results
    )
    return snippets


# ----------------------------------------------------------------------
# 2) LLM helper (Gemma 3 via Ollama)
# ----------------------------------------------------------------------
def invoke_ollama(prompt: str ) -> str:
    """
    Send a prompt to the local Ollama instance and return Gemma's response.
    Ollama must be running: `ollama serve` (starts automatically on the first call).
    """
    body = {"model": "gemma3:1b", "prompt": prompt, "stream": False}
    resp = requests.post("http://localhost:11434/api/generate", json=body, timeout=120)
    
    resp.raise_for_status()
    return resp.json()["response"]


# ----------------------------------------------------------------------
# 3) Demo run
# ----------------------------------------------------------------------
if __name__ == "__main__":
    question = "What is the newest exoplanet confirmed by NASA?"

    # 1. Get live context
    print("🔍  Searching the web …")
    context = web_search(question)

    # 2. Build a grounded prompt
    prompt = (
        "Answer the question using ONLY the context below. "
        "If the context is insufficient, say you don't know.\n\n"
        f"### CONTEXT\n{context}\n\n"
        f"### QUESTION\n{question}\n### ANSWER:"
    )

    # 3. Ask Gemma-3 (1 B)
    print("🤖  Querying Gemma 3 (1 B) …")
    answer = invoke_ollama(prompt)
    print("\n=== Gemma 3 Answer ===\n")
    print(answer.strip())