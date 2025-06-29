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

    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": max_results,
        "search_depth": "advanced",
    }
    resp = requests.post("https://api.tavily.com/search", json=payload, timeout=30)
    resp.raise_for_status()

    results = resp.json()
    print(results)

    # results = resp.json()["results"]
    # # snippets = "\n".join(
    # #     f"{item['title']}\n{shorten(item['content'], 250)}"
    # #     for item in results
    # # )
    # snippets = "\n".join(
    #     f"{item['title']}\n{(item['content'])}\n\n"
    #     for item in results
    # )
    # return snippets

print(web_search("Isreal and Iran war"))