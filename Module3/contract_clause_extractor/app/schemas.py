# =============================================================================
# schemas.py — defines what a valid extraction must look like (Project 3.2)
# =============================================================================
# After the LLM returns JSON, we check it against these models.
# If a field is missing or wrong (e.g. a made-up clause type), validation fails.
# =============================================================================

from typing import Literal

from pydantic import BaseModel, Field


class Clause(BaseModel):
    
    clause_type: Literal[
        "termination",
        "liability",
        "payment",
        "confidentiality",
        "governing_law",
        "other",
    ]
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    excerpt: str = Field(min_length=1)
    risk_level: Literal["low", "medium", "high"] = "medium"


class ContractExtraction(BaseModel):
    # The full answer from the LLM — everything we need about one contract.

    
    contract_title: str = Field(min_length=1)
    
    parties: list[str] = Field(min_length=1)
     
    effective_date: str | None = None
     
    clauses: list[Clause] = Field(min_length=1)


def extraction_json_schema() -> dict:
    # A simple description of the JSON shape we paste into the LLM prompt.
    
    return {
        "contract_title": "string",
        "parties": ["string"],
        "effective_date": "string or null",
        "clauses": [
            {
                "clause_type": "termination | liability | payment | confidentiality | governing_law | other",
                "title": "string",
                "summary": "string",
                "excerpt": "short quote from contract",
                "risk_level": "low | medium | high",
            }
        ],
    }