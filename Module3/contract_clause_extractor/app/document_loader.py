from pathlib import Path

from pypdf import PdfReader

ALLOWED_EXTENSIONS = {".pdf", ".txt"}


def load_contract_text(uploaded_file_path: str|None,pasted_text:str) -> str:

    if pasted_text and pasted_text.strip():
        return pasted_text.strip()
    
    if not uploaded_file_path:
        raise ValueError("No file uploaded and no text pasted.")

    
    path = Path(uploaded_file_path)
    extension = path.suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    if extension == ".txt":
        return path.read_text(encoding="utf-8").strip()

    reader = PdfReader(str(path))
    pages = [page.extract_text() for page in reader.pages]
    text = "\n".join(pages).strip()

    if not text:
        raise ValueError("No text found in the file.")

    return text