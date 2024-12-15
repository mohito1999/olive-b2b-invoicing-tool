import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure OpenAI API Configuration
AZURE_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT").rstrip("/") + "/"
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Function to Interact with Azure OpenAI
def get_llm_response(prompt: str, max_tokens: int = 100):
    try:
        # Define Headers
        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_API_KEY
        }

        # Define Request Body
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }

        # Construct Full Endpoint URL
        url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_MODEL}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"

        # Make the POST Request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Extract Response
        result = response.json()

        # Extract Message or Raise Error
        if "choices" in result and "message" in result["choices"][0]:
            content = result["choices"][0]["message"]["content"].strip()
            print(f"[Azure LLM] Routed to: {content}")
            return content
        else:
            raise ValueError("Unexpected response structure from Azure OpenAI.")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error during Azure OpenAI API call: {str(e)}")
