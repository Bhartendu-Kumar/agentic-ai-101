#!/usr/bin/env python3
# simple_web_llm.py  –  minimal web-search + local LLM

import sys, requests, json

# ---------- 1. plain web search (DuckDuckGo Instant Answer) ----------
query = " ".join(sys.argv[1:]) or "Who is the CEO of Nvidia?"        # allow CLI arg
rsp  = requests.get(
        "https://api.duckduckgo.com/",
        params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
        timeout=10
      ).json()

snippet = rsp.get("AbstractText") or rsp.get("Answer") or "No snippet found."
print("🔎  Search snippet:\n", snippet)

# ---------- 2. send the snippet to Ollama ----------------------------
prompt = f"Answer the question using this snippet only:\n\n{snippet}\n\nQ: {query}\nA:"
resp = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "gemma3:1b", "prompt": prompt, "stream": False},
        timeout=60
      ).json()

print("\n🤖  gemma3:1b says:\n", resp["response"])