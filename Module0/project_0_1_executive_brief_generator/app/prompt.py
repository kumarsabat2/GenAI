def get_system_prompt() -> str:
    return """
    You are an communication assistant.
    The executive brief should be 1-2 paragraphs long.    
    """
def build_brief_user_prompt(topic: str, source_text: str) -> str:
    return f"""
    Topic: {topic}
    Source text: {source_text}
    Generate an executive brief for the.
    
    """