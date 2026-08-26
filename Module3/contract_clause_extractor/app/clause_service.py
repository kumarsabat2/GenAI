import json
from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from app.document_loader import load_contract_text
from app.guardrails import validate_contract_text
from app.llm_service import call_llm_json
from app.prompts import build_extraction_user_prompt, get_extraction_system_prompt
from app.schemas import ContractExtraction

CLAUSE_COLUMNS =[
    "Clause Type",
    "Title",
    "Summary",
    "Risk Level",
    "Excerpt",
]


EMPTY_CLAUSE_DF = pd.DataFrame(columns=CLAUSE_COLUMNS)


def load_sample_nda_text() -> str:
    sample_path = Path(__file__).resolve().parent.parent/"data"/"sample_nda.txt"
    return sample_path.read_text(encoding="utf-8").strip()


def _error_outputs(message:str):
    return message,"{}", EMPTY_CLAUSE_DF


def _resolve_file_path(uploaded_file)-> str|None:

    if not uploaded_file:
        return None
    
    if isinstance(uploaded_file, str):
        return uploaded_file
    
    if isinstance(uploaded_file, dict):
        return uploaded_file.get("path") or uploaded_file.get("name")

    return getattr(uploaded_file, "name", None)


def extract_contract_clauses(uploaded_file, pasted_text:str):

    try:
        file_path = _resolve_file_path(uploaded_file)
        contract_text = load_contract_text(file_path, pasted_text)
    except ValueError as error:
        return _error_outputs(str(error))


    allowed, message = validate_contract_text(contract_text)
    
    if not allowed:
        return _error_outputs(message)

    
    try:
        system_prompt = get_extraction_system_prompt()
        user_prompt = build_extraction_user_prompt(contract_text)

        raw_data = call_llm_json(system_prompt, user_prompt)

        extraction = ContractExtraction.model_validate(raw_data)

    except Exception as error:
        return _error_outputs(f"Error extracting clauses: {str(error)}")


    clause_rows = [
        {
            "Clause Type": clause.clause_type,
            "Title": clause.title,
            "Summary": clause.summary,
             "Risk Level": clause.risk_level,
            "Excerpt": clause.excerpt,
           
        }

        for clause in extraction.clauses
    ]

    clause_df = pd.DataFrame(clause_rows, columns=CLAUSE_COLUMNS)

    high_risk = sum(1 for clause in extraction.clauses if clause.risk_level == "high")


    summary_md = (
        f"### Extraction complete\n\n"
        f"**Contract:** {extraction.contract_title}\n\n"
        f"**Parties:** {', '.join(extraction.parties)}\n\n"
        f"**Effective date:** {extraction.effective_date or 'Not specified'}\n\n"
        f"**Clauses found:** {len(extraction.clauses)} "
        f"({high_risk} high-risk)"
    )

    pretty_json = json.dumps(extraction.model_dump(), indent=4)

    return summary_md, pretty_json, clause_df

