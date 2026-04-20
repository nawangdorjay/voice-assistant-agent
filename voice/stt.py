"""
Speech-to-Text Module
Supports Whisper API (cloud) and Vosk (offline).
"""
import os
import tempfile
from typing import Optional


# Language code mapping for Whisper
WHISPER_LANG_MAP = {
    "hi": "hi",  # Hindi
    "bn": "bn",  # Bengali
    "ta": "ta",  # Tamil
    "te": "te",  # Telugu
    "mr": "mr",  # Marathi
    "gu": "gu",  # Gujarati
    "kn": "kn",  # Kannada
    "ml": "ml",  # Malayalam
    "pa": "pa",  # Punjabi
    "or": "or",  # Odia
    "en": "en",  # English
}


def transcribe_audio(audio_path: str, language: Optional[str] = None) -> dict:
    """
    Transcribe audio file to text.

    Args:
        audio_path: Path to audio file (wav, mp3, m4a, etc.)
        language: Optional language hint (e.g., 'hi', 'en')

    Returns:
        dict with 'text', 'language', and 'confidence'
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")

    if api_key:
        return _transcribe_whisper(audio_path, language, api_key)
    else:
        return {
            "text": "",
            "language": "en",
            "error": "No API key found. Set OPENAI_API_KEY or GROQ_API_KEY.",
        }


def _transcribe_whisper(audio_path: str, language: Optional[str], api_key: str) -> dict:
    """Transcribe using OpenAI Whisper API."""
    try:
        import openai
    except ImportError:
        return {"text": "", "error": "openai package not installed"}

    is_groq = "groq" in api_key.lower()

    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1" if is_groq else None,
    )

    try:
        with open(audio_path, "rb") as audio_file:
            # Groq uses whisper-large-v3, OpenAI uses whisper-1
            model = "whisper-large-v3" if is_groq else "whisper-1"

            kwargs = {
                "model": model,
                "file": audio_file,
                "response_format": "verbose_json",
            }
            if language and language in WHISPER_LANG_MAP:
                kwargs["language"] = WHISPER_LANG_MAP[language]

            result = client.audio.transcriptions.create(**kwargs)

            # Detect language from response
            detected_lang = getattr(result, "language", language or "en")

            return {
                "text": result.text,
                "language": detected_lang,
                "confidence": 0.9,  # Whisper doesn't return confidence
            }

    except Exception as e:
        return {"text": "", "error": str(e)}


def transcribe_audio_bytes(audio_bytes: bytes, language: Optional[str] = None) -> dict:
    """Transcribe audio from bytes (for Streamlit/Gradio file upload)."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        return transcribe_audio(tmp_path, language)
    finally:
        os.unlink(tmp_path)
