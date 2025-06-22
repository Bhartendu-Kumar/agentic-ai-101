# pip install ollama tavily-python dotenv 
# # Pull the tool-enabled Gemma 3
# ollama pull orieg/gemma3-tools:1b
# # (or try `aliafshar/gemma3-it-qat-tools:1b` if you like)

# from ollama import Client
# client = Client(host="http://127.0.0.1:11434", timeout=120)


import os, json, ollama
from tavily import TavilyClient

tavily = TavilyClient(os.getenv("TAVILY_API_KEY"))

def web_search(query: str, k: int = 5) -> str:
    hits = tavily.search(query=query, max_results=k)["results"]
    return "\n".join(f"{h['title']}\n{h['content']}" for h in hits)

tools = [{
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the live web and return top snippets.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "k":     {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    }
}]

client = ollama.Client()
MODEL = "orieg/gemma3-tools:1b"          # Gemma-3 variant with tool support

def ask(prompt: str) -> None:
    rsp = client.chat(model=MODEL, messages=[{"role": "user", "content": prompt}], tools=tools)
    if "tool" in rsp:                                 # model requested the tool
        args = json.loads(rsp["tool"]["function"]["arguments"])
        follow = client.chat(
            model=MODEL,
            messages=[{"role": "tool", "name": "web_search", "content": web_search(**args)}]
        )
        print(follow["message"]["content"])
    else:
        print(rsp["message"]["content"])

if __name__ == "__main__":
    ask("What is the newest exoplanet confirmed by NASA?")