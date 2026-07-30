import os

from gtts import gTTS
from app.core.config import AUDIO_OUTPUT_PATH


def text_to_speech(text: str, language_code: str, output_path: str = AUDIO_OUTPUT_PATH) -> str:
    """Convert text to speech and save as MP3. Returns the output file path."""
    if not text.strip():
        raise ValueError("Text for speech synthesis cannot be empty.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tts = gTTS(text=text, lang=language_code, slow=False)
    tts.save(output_path)
    return output_path