import requests

def invoke_ollama():
	model = "gemma3:1b"  # Change this to your preferred model

	body = {
		"model": model,
		# "prompt": "hi",
		"messages": [
			{
				"role": "system",
				"content": "You are a helpful assistant that can answer questions and help with tasks."
			},
			{
				"role": "user",
				"content": "Hello! Can you tell me a fun fact about programming?"
			}
		],
		"stream": False
	}

	response = requests.post(
		"http://localhost:11434/api/chat",
		json=body
	)

	response_data = response.json()
	print(response_data['message']['content'])

invoke_ollama()