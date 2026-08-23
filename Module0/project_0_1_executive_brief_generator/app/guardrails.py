def validate_brief_input(topic: str, source_text: str) -> bool:
     if not topic or not source_text:
        return False, "Topic and source text are required"
     if len(topic) > 100:
        return False, "Topic must be less than 100 characters"
     if len(source_text) > 1000:
        return False, "Source text must be less than 1000 characters"
     return True, "Input is valid"