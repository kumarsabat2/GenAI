from app.llm_service import call_llm
from app.prompt import get_system_prompt, build_brief_user_prompt
from app.guardrails import validate_brief_input

def generate_brief(topic: str, source_text: str) -> str:
    is_valid, error_message = validate_brief_input(topic, source_text)
    if not is_valid:
        raise ValueError(error_message)
    system_prompt = get_system_prompt()
    user_prompt = build_brief_user_prompt(topic, source_text)
    brief=call_llm(system_prompt, user_prompt)
    return brief