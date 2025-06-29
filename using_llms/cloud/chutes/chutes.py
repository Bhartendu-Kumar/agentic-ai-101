import requests
import json

def invoke_chute():
	api_token = "cpk_6184f07af90b4a9583f555710a1ada7a.dcb3e11110c85fd79aac1cc6823a18d0.txPORnOOZ7fOPBGX6kvdYEGzJe6rk9wS"  # Replace with your actual API token

	headers = {
		"Authorization": "Bearer " + api_token,
		"Content-Type": "application/json"
	}
	
	body = {
		"model": "deepseek-ai/DeepSeek-V3-0324",
		# "model": "deepseek-ai/DeepSeek-V3-Base",
		"messages": [
			{
				"role": "system",
				"content": "You are a helpful assistant that can answer questions and help with tasks."
			},
			{
				"role": "user",
				"content": "What is the weather in Tokyo?"
			},	
			
		],
		"stream": False,
		"max_tokens": 1024,
		"temperature": 0.7
	}

	response = requests.post(
		"https://llm.chutes.ai/v1/chat/completions",
		headers=headers,
		json=body
	)
	print(response.json())
	# response.raise_for_status()  # Still good to keep for basic HTTP error checking
	
	# response_data = response.json()
	
	# # # Print the relevant part of the response
	# # # This assumes the API call is successful and the response structure is as expected.
	# print(response_data["choices"][0]["message"]["content"])

invoke_chute()