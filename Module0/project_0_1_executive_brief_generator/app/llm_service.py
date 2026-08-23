import json
import regex as re
import time

from openai import OpenAI

from app.config import (
    get_openai_api_key,
    get_openai_model,
    get_model_provider,
)

def get_client_and_model():
    provider = get_model_provider()
    if provider == "openai":
        client = OpenAI(api_key=get_openai_api_key())
        model = get_openai_model()
        return client, model, provider
    raise ValueError(f"Unsupported model provider: {provider}")   

def call_llm(system_prompt: str, user_prompt: str,temperature: float = 0.2) -> str:

    client, model,provider = get_client_and_model()
    print(f"using {provider} to call {model} with temperature {temperature}")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
    )
    if response.usage:
        print(f"Tokens used: {response.usage.total_tokens}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Completion tokens: {response.usage.completion_tokens}")
    return response.choices[0].message.content