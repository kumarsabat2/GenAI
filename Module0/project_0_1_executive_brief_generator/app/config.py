import os

from dotenv import load_dotenv
load_dotenv()

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

print(MODEL_PROVIDER)
print(OPENAI_API_KEY)
print(OPENAI_MODEL)

def get_model_provider():
    return MODEL_PROVIDER

def get_openai_api_key():
    if OPENAI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY is not set")
    return OPENAI_API_KEY

def get_openai_model():
    return OPENAI_MODEL
