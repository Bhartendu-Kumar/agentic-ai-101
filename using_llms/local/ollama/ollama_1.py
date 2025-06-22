import requests

def invoke_ollama():
	model = "gemma3:1b"  # Change this to your preferred model

	body = {
		"model": model,
		"prompt": "hi",
		"stream": False
	}

	response = requests.post(
		"http://localhost:11434/api/generate",
		json=body
	)

	response_data = response.json()
	print(response_data["response"])

invoke_ollama()