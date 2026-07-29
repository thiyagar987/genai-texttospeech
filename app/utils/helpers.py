from app.core.config import MAX_TEXT_LENGTH


def truncate_text(text: str) -> str:
    """Truncate text to the maximum allowed length."""
    if len(text) > MAX_TEXT_LENGTH:
        return text[:MAX_TEXT_LENGTH]
    return text


def read_audio_bytes(file_path: str) -> bytes:
    """Read audio file and return bytes for Streamlit download."""
    with open(file_path, "rb") as f:
        return f.read()