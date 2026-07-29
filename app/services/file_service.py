import pandas as pd
import PyPDF2
import io


def extract_text_from_file(uploaded_file) -> str:
    """Extract text content from TXT, PDF, CSV, or Excel files."""
    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    if filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        return df.to_string(index=False)

    if filename.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        return df.to_string(index=False)

    raise ValueError(f"Unsupported file type: {uploaded_file.name}")