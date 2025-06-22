import requests
import json

def chat_with_gemma():
    """
    Simple example of using Ollama's API to chat with the Gemma3:1b model.
    Make sure Ollama is running locally with: ollama serve
    And that you have the model pulled: ollama pull gemma2:2b
    """

    # Ollama API endpoint (default local installation)
    url = "http://localhost:11434/api/generate"

    # Prepare the request payload
    payload = {
        "model": "gemma2:2b",  # Using gemma2:2b as it's more commonly available
        "prompt": "Hello! Can you tell me a fun fact about artificial intelligence?",
        "stream": False  # Set to False to get the complete response at once
    }

    try:
        # Make the API request
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the JSON response
        result = response.json()

        # Print the model's response
        print("Gemma2 says:")
        print(result["response"])

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Make sure Ollama is running with 'ollama serve'")
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except KeyError as e:
        print(f"Error parsing response: {e}")
        print("Full response:", response.text)

def chat_with_streaming():
    """
    Example of streaming response from Ollama (like ChatGPT-style typing effect)
    """
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "gemma2:2b",
        "prompt": "Write a short poem about coding in Python.",
        "stream": True  # Enable streaming
    }

    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()

        print("Gemma2 streaming response:")
        print("-" * 40)

        # Process the streaming response
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    if 'response' in chunk:
                        print(chunk['response'], end='', flush=True)
                    if chunk.get('done', False):
                        print("\n" + "-" * 40)
                        break
                except json.JSONDecodeError:
                    continue

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Make sure Ollama is running with 'ollama serve'")
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

def list_available_models():
    """
    List all models available in your local Ollama installation
    """
    url = "http://localhost:11434/api/tags"

    try:
        response = requests.get(url)
        response.raise_for_status()

        models = response.json()
        print("Available Ollama models:")
        print("-" * 30)

        if 'models' in models:
            for model in models['models']:
                print(f"- {model['name']} (Size: {model.get('size', 'Unknown')})")
        else:
            print("No models found. Try pulling a model with: ollama pull gemma2:2b")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Make sure Ollama is running with 'ollama serve'")
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    print("=== Ollama Gemma2 Hello World ===\n")

    # First, list available models
    list_available_models()
    print()

    # Simple chat example
    chat_with_gemma()
    print()

    # Streaming example
    chat_with_streaming()

    print("\nDone! If you got connection errors, make sure to:")
    print("1. Start Ollama: ollama serve")
    print("2. Pull the model: ollama pull gemma2:2b")
    print("3. Or use a different model that you have installed")