import os, json, requests
from tavily import TavilyClient

MODEL  = "orieg/gemma3-tools:1b"
TAVILY = TavilyClient(os.getenv("TAVILY_API_KEY"))

def web_search(query, k=5):
    hits = TAVILY.search(query=query, max_results=k)["results"]
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

def chat(payload):
    url = "http://localhost:11434/api/chat"      # <- chat, not generate
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()

def ask(question):
    # 1st round – let the model decide if it wants the tool
    msg = [{"role": "user", "content": question}]
    out = chat({"model": MODEL, "messages": msg, "tools": tools, "stream": False})

    if "tool" in out:                           # model picked web_search
        args = json.loads(out["tool"]["function"]["arguments"])
        result = web_search(**args)
        msg.append({"role": "tool", "name": "web_search", "content": result})
        out = chat({"model": MODEL, "messages": msg, "stream": False})

    print(out["message"]["content"])

if __name__ == "__main__":
    ask("What is the newest exoplanet confirmed by NASA?")