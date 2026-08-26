# =============================================================================
# llm_service.py — talk to OpenAI, DeepSeek, or Ollama (Project 3.2)
# =============================================================================
# All API calls go through this file.
# This project mainly uses call_llm_json() to get structured JSON back.
# =============================================================================

import json
import re

from openai import OpenAI

from app.config import (
    get_deepseek_api_key,
    get_deepseek_model,
    get_model_provider,
    get_openai_api_key,
    get_openai_model,
)


def get_client_and_model():
    
    provider = get_model_provider()

    # OpenAI — default for course demos; supports JSON mode.
    if provider == "openai":
        client = OpenAI(api_key=get_openai_api_key())
        model = get_openai_model()
        return client, model, provider

    # DeepSeek — same OpenAI-style API, different URL and key.
    if provider == "deepseek":
        client = OpenAI(
            api_key=get_deepseek_api_key(),
            base_url="https://api.deepseek.com",
        )
        model = get_deepseek_model()
        return client, model, provider

   

    raise ValueError(
        "Unsupported MODEL_PROVIDER. Use 'openai', 'deepseek'."
    )


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
    # Send a chat message and get plain text back.
    
    client, model, provider = get_client_and_model()

    print(f"\nUsing provider: {provider}")
    print(f"Using model: {model}")

    # Send system + user messages to the API.
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )

    # Print token usage to the terminal so students can see cost.
    if response.usage:
        print("\n=== TOKEN USAGE ===")
        print("Prompt Tokens:", response.usage.prompt_tokens)
        print("Completion Tokens:", response.usage.completion_tokens)
        print("Total Tokens:", response.usage.total_tokens)

    return response.choices[0].message.content


def _parse_json_response(raw_text: str) -> dict:
    # This function pulls out the JSON and turns it into a Python dict.
    text = raw_text.strip()

    # Look for ```json { ... } ``` first — most common format.
    fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)
    else:
        # No fences — try to find the first { ... } block in the text.
        brace_match = re.search(r"\{.*\}", text, re.DOTALL)
        if brace_match:
            text = brace_match.group(0)

    return json.loads(text)


def call_llm_json(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.1,
) -> dict:
    client, model, provider = get_client_and_model()

    print(f"\nUsing provider: {provider}")
    print(f"Using model: {model}")

    # Build the API request — system message, user message, low temperature.
    request_kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }


    if provider == "openai":
        request_kwargs["response_format"] = {"type": "json_object"}

    # Call the API and wait for the response.
    response = client.chat.completions.create(**request_kwargs)

    # Print how many tokens we used.
    if response.usage:
        print("\n=== TOKEN USAGE ===")
        print("Prompt Tokens:", response.usage.prompt_tokens)
        print("Completion Tokens:", response.usage.completion_tokens)
        print("Total Tokens:", response.usage.total_tokens)

    # Get the text from the response and parse it into a dict.
    raw_text = response.choices[0].message.content or ""
    return _parse_json_response(raw_text)