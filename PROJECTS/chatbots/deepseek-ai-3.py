# Chat With Chute - DeepSeek Bot

# Before running the program, run the below commands to set the API Key in terminal

# For Windows
# $env:CHUTES_API_TOKEN="your_api_token"

# For Linux or macOS
# export CHUTES_API_TOKEN="your_api_token"

# =================================================================================


import aiohttp
import asyncio
import json
import os


async def chat_with_chute():
	api_token = os.getenv("CHUTES_API_TOKEN")
	if not api_token:
		print("Please set the CHUTES_API_TOKEN environment variable.")
		return

	print("CHUTES_API_TOKEN is set.\nType 'exit' or 'quit' to end the conversation.\n")

	headers = {
		"Authorization": "Bearer " + api_token,
		"Content-Type": "application/json"
	}

	# Conversation history
	messages = []

	while True:
		user_input = input("You: ").strip()
		if user_input.lower() in ("exit", "quit", "e"):
			print("Exiting chat. Goodbye!\n================================")
			break

		messages.append({"role": "user", "content": user_input})

		body = {
			"model": "deepseek-ai/DeepSeek-V3-0324",
			"messages": messages,
			"stream": True,
			"max_tokens": 1024,
			"temperature": 0.7
		}

		async with aiohttp.ClientSession() as session:
			async with session.post(
				"https://llm.chutes.ai/v1/chat/completions",
				headers=headers,
				json=body
			) as response:
				if response.status != 200:
					text = await response.text()
					print(f"Request failed: {response.status}\n{text}")
					continue

				print("DeepSeek Bot:", end=" ", flush=True)
				full_reply = ""
				async for line in response.content:
					line = line.decode("utf-8").strip()
					if not line or not line.startswith("data: "):
						continue

					data = line[6:]
					if data == "[DONE]":
						break

					try:
						parsed = json.loads(data)
						content = parsed["choices"][0]["delta"].get("content")
						if content:
							print(content, end="", flush=True)
							full_reply += content
					except Exception as e:
						print(f"\nError parsing chunk: {e}")

				print("\n")
				messages.append({"role": "assistant", "content": full_reply})


# Run the chatbot
asyncio.run(chat_with_chute())
