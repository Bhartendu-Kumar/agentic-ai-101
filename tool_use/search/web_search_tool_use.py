import os, json, requests
from tavily import TavilyClient


TAVILY = "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"

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

def chat(body):
    resp = requests.post("http://localhost:11434/api/chat", json=body, timeout=120)
    resp.raise_for_status()
    return resp.json()

def ask():
    # 1st round – let the model decide if it wants the tool
    msg = [{"role": "system", "content": "You are a helpful assistant that can use the web tool to answer questions. \
            If you want to use the web for this query, output this format: <WEB_USE> Yes/No </WEB_USE>. Example: <WEB_USE> Yes </WEB_USE>. Example: <WEB_USE> No </WEB_USE>.\
            If you are saying Yes for <WEB_USE> Yes </WEB_USE>, then you should give the search query to the web tool. For that include your query in this format: <WEB_SEARCH> <query> </WEB_SEARCH>. Example: <WEB_SEARCH> Today's oil price in India </WEB_SEARCH>. Example: <WEB_SEARCH> What is the weather in Tokyo? </WEB_SEARCH>."},
        {"role": "user", "content": "Today's oil price in India?"}]
    body = {"model": "orieg/gemma3-tools:1b", "messages": msg, "tools": tools, "stream": False}
    out = chat(body)
    #print the out
    print("--------------------------------")
    print("First round")
    print(out)
    print("First round done")
    print("--------------------------------")
    print("tool")
    print(out["tool"])
    print("--------------------------------")


    if "tool" in out:                           # model picked web_search
        args = json.loads(out["tool"]["function"]["arguments"])
        result = web_search(**args)
        msg.append({"role": "tool", "name": "web_search", "content": result})
        out = chat({"model": "model", "messages": msg, "stream": False})

    print(out["message"]["content"])

if __name__ == "__main__":
    ask()