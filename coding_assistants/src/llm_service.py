import os
import requests
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        print(f"Loaded API Key: {self.api_key}") # for debugging
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def get_response(self, system_prompt: str, user_prompt: str):
        """
        Sends a request to the OpenRouter API and returns the LLM's response.
        """
        if not self.api_key:
            return "Error: OPENROUTER_API_KEY not found. Please set it in your .env file."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            return f"Error communicating with OpenRouter API: {e}"
