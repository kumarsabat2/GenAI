# =============================================================================
# prompts.py — the words we send to the LLM (Project 3.2)
# =============================================================================
# Holds the system and user messages that tell the model how to extract clauses.
# =============================================================================

import json

from app.schemas import extraction_json_schema


def get_extraction_system_prompt() -> str:
    return """
You are a legal contract analysis assistant for business teams.

Extract key clauses from contract text into structured JSON.

Rules:
- Return valid JSON only (no markdown fences).
- Use excerpts copied from the source text when possible.
- If a clause type is missing, omit it (do not invent clauses).
- Assign risk_level based on business impact (high = large liability / strict terms).
- If effective date is unknown, set effective_date to null.
"""


def build_extraction_user_prompt(contract_text: str) -> str:
    
    schema = json.dumps(extraction_json_schema(), indent=2)

    return f"""
Analyze the contract below and extract clauses.

Focus on these clause types when present:
- termination
- liability
- payment
- confidentiality
- governing law
- other (for important clauses that do not fit above)

Required JSON shape:
{schema}

CONTRACT TEXT:
{contract_text}
"""