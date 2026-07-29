from app.api.gemini_client import get_gemini_client


def translate_text(text: str, target_language: str) -> str:
    """Translate text to the target language using Gemini API."""
    if not text.strip():
        raise ValueError("Input text cannot be empty.")

    client = get_gemini_client()
    prompt = (
        f"Translate the following text to {target_language}. "
        f"Return only the translated text without any explanation or extra content.\n\n"
        f"Text: {text}"
    )
    response = client.generate_content(prompt)
    return response.text.strip()