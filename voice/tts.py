"""
Text-to-Speech Module
Supports gTTS (free, cloud) with offline fallback.
"""
import os
import tempfile
from typing import Optional


# gTTS language codes
GTTS_LANG_MAP = {
    "hi": "hi",  # Hindi
    "bn": "bn",  # Bengali
    "ta": "ta",  # Tamil
    "te": "te",  # Telugu
    "mr": "mr",  # Marathi
    "gu": "gu",  # Gujarati
    "kn": "kn",  # Kannada
    "ml": "ml",  # Malayalam
    "pa": "pa",  # Punjabi
    "or": "or",  # Odia (limited support)
    "en": "en",  # English
}


def synthesize_speech(text: str, language: str = "en", slow: bool = False) -> Optional[str]:
    """
    Convert text to speech and return path to audio file.

    Args:
        text: Text to speak
        language: Language code (hi, en, ta, etc.)
        slow: Speak slowly (useful for clear pronunciation)

    Returns:
        Path to generated MP3 file, or None on failure
    """
    if not text or not text.strip():
        return None

    # Clean text for TTS (remove markdown, emojis)
    clean_text = _clean_text(text)

    gtts_lang = GTTS_LANG_MAP.get(language, "en")
    return _synthesize_gtts(clean_text, gtts_lang, slow)


def synthesize_speech_bytes(text: str, language: str = "en", slow: bool = False) -> Optional[bytes]:
    """
    Convert text to speech and return audio bytes.
    Useful for streaming responses in web UIs.
    """
    path = synthesize_speech(text, language, slow)
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    return None


def _synthesize_gtts(text: str, language: str, slow: bool) -> Optional[str]:
    """Synthesize using Google Text-to-Speech."""
    try:
        from gtts import gTTS
    except ImportError:
        return None

    try:
        tts = gTTS(text=text, lang=language, slow=slow)
        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tts.save(tmp.name)
        return tmp.name
    except Exception:
        return None


def _clean_text(text: str) -> str:
    """Remove markdown, emojis, and formatting for cleaner TTS output."""
    import re

    # Remove markdown headers
    text = re.sub(r'#{1,6}\s*', '', text)
    # Remove bold/italic markers
    text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove code blocks
    text = re.sub(r'```[^`]*```', '', text)
    # Remove inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove bullet points but keep content
    text = re.sub(r'^[\s]*[-•*]\s*', '', text, flags=re.MULTILINE)
    # Remove numbered list dots but keep numbers
    text = re.sub(r'^(\d+)\.\s*', r'\1: ', text, flags=re.MULTILINE)
    # Remove emojis (basic range)
    text = re.sub(r'[🚨✅⚠️❌💡📌🏥🌾💊🔊🎤🤖⛰️]', '', text)
    # Collapse whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)

    return text.strip()
