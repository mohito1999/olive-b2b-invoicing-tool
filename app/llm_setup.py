import openai
import os

def get_llm():
    openai.api_type = "azure"
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = os.getenv("AZURE_OPENAI_VERSION")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    return openai

def get_llm_response(prompt: str, max_tokens: int = 100):
    openai = get_llm()
    response = openai.Completion.create(
        engine=os.getenv("AZURE_OPENAI_MODEL"),
        prompt=prompt,
        max_tokens=max_tokens,
    )
    return response["choices"][0]["text"].strip()
