# pip install ollama tavily-python dotenv 
# # Pull the tool-enabled Gemma 3
# ollama pull orieg/gemma3-tools:1b
# # (or try `aliafshar/gemma3-it-qat-tools:1b` if you like)


import os, json, ollama
from tavily import TavilyClient                     # simple REST wrapper

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "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")
tavily = TavilyClient(TAVILY_API_KEY)

def web_search(query: str, k: int = 5) -> str:
    """Call Tavily and format chunky snippets for the model."""
    hits = tavily.search(query=query, max_results=k)["results"]
    return "\n".join(f"{h['title']}\n{h['content']}" for h in hits)

tools = [
    {  # JSON schema that Ollama expects
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
    }
]

client = ollama.Client()

def ask(prompt):
    stream = client.chat(
        model="orieg/gemma3-tools:1b",
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
        stream=True)
    function_args = None
    for chunk in stream:
        if "tool" in chunk:                     # model wants to call the tool
            function_args = json.loads(chunk["tool"]["function"]["arguments"])
            break                               # 1 tool call expected here
        else:
            print(chunk["message"]["content"], end="", flush=True)

    if function_args:
        results = web_search(**function_args)
        follow_up = client.chat(
            model="orieg/gemma3-tools:1b",
            messages=[
              {"role": "tool", "name": "web_search", "content": results}
            ],
        )
        print(follow_up["message"]["content"])

if __name__ == "__main__":
    ask("What is the newest exoplanet confirmed by NASA?")