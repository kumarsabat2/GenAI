# =============================================================================
# guardrails.py — check contract text before we call the LLM (Project 3.2)
# =============================================================================
# Cheap checks that save API cost: reject bad input before we send it to the model.
# =============================================================================

# Do not accept contracts longer than this (keeps demo cost predictable).
MAX_CONTRACT_CHARS = 50_000

# Do not accept contracts shorter than this (too little text to find real clauses).
MIN_CONTRACT_CHARS = 200


def validate_contract_text(contract_text: str) -> tuple[bool, str]:
   
    if not contract_text or not contract_text.strip():
        return False, "Contract text is empty."

    # How many characters after trimming spaces at the ends.
    length = len(contract_text.strip())

    # Too short — probably not a real contract.
    if length < MIN_CONTRACT_CHARS:
        return False, (
            f"Contract text is too short ({length} chars). "
            f"Minimum is {MIN_CONTRACT_CHARS} characters."
        )

    # Too long — would be expensive and may not fit in the model context.
    if length > MAX_CONTRACT_CHARS:
        return False, (
            f"Contract text is too long ({length} chars). "
            f"Maximum is {MAX_CONTRACT_CHARS} characters."
        )

    # All checks passed.
    return True, "Input allowed."