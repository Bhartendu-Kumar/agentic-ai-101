#!/usr/bin/env python3
# search_and_answer.py
import sys, requests, json
from duckduckgo_search import DDGS

query = " ".join(sys.argv[1:]) or "Who is the CEO of Nvidia?"

# 1. Web snippet
with DDGS() as d:
    hits = d.text(query, max_results=1)
    first = hits[0] if isinstance(hits, list) else next(hits, {})
snippet = first.get("body", "No snippet found.")

print("🔎  Snippet:", snippet)

# 2. Local LLM answer
prompt = f"Use only this snippet to answer:\n\n{snippet}\n\nQ: {query}\nA:"
resp = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "gemma3:1b", "prompt": prompt, "stream": False},
    timeout=60
).json()

if "response" in resp:
    print("\n🤖  gemma3:1b says:", resp["response"].strip())
else:
    print("\n❌  Ollama error:", resp.get("error", resp))