
import os, json, requests
from tavily import TavilyClient

tavily = TavilyClient(os.getenv("TAVILY_API_KEY"))
MODEL  = "orieg/gemma3-tools:1b"       # a Gemma-3 build that supports tools
API    = "http://localhost:11434/api/chat"

def web_search(query: str, k: int = 5) -> str:
    hits = tavily.search(query=query, max_results=k)["results"]
    return "\n".join(f"{h['title']}\n{h['content']}" for h in hits)

tools = [{
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Look up fresh facts.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "k": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    }
}]

def ask(question: str):
    # 1️⃣ send the user message + tool declarations
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": question}],
        "tools": tools,
        "stream": False
    }
    rsp = requests.post(API, json=body, timeout=120).json()

    # 2️⃣ if the model asked for the tool, run it and continue the chat
    if "tool" in rsp:
        args = json.loads(rsp["tool"]["function"]["arguments"])
        result = web_search(**args)

        follow_up = {
            "model": MODEL,
            "messages": [
                {"role": "tool", "name": "web_search", "content": result}
            ],
            "stream": False
        }
        final = requests.post(API, json=follow_up, timeout=120).json()
        print(final["message"]["content"])
    else:
        print(rsp["message"]["content"])

if __name__ == "__main__":
    ask("What is the newest exoplanet confirmed by NASA?")