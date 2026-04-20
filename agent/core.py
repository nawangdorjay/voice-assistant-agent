"""
Voice-First Accessibility Agent — Core Logic
Orchestrates voice input → text processing → tool execution → voice output.
Designed for low-literacy users in rural India.
"""
import os
import json
from typing import Optional, List, Dict, Any
from agent.tools import get_tools, execute_tool

SYSTEM_PROMPT = """You are Sahayak (सहायक — Helper), a voice-first AI assistant for people in rural and remote India.

You communicate entirely through voice. Most users cannot read or type well, so your responses MUST be:
1. SHORT — 2-3 sentences maximum for each point
2. SIMPLE — use common words, no jargon
3. SPOKEN-STYLE — write as you would speak, not as you would write
4. STRUCTURED — break complex answers into numbered steps

IMPORTANT RULES:
- ALWAYS respond in the same language the user speaks in
- For Hindi queries, respond in Hindi (written in Devanagari script)
- If user says something unclear, ask a simple clarifying question
- For emergencies (health, disaster), give the action FIRST, then details
- Never give medical diagnosis — direct to 108/hospital
- Use local units: km, °C, ₹, quintal, bigha
- Mention phone numbers verbally (e.g., "one zero eight" for 108)

Your capabilities:
- Farming advice: crops, weather, pests, market prices
- Health info: symptoms, nearest hospital, emergency numbers
- Government schemes: eligibility, how to apply
- General knowledge: weather, directions, time, calculations
- Local information: markets, transport, contacts

Keep every response under 30 seconds of speaking time. Speak like a helpful neighbor, not a textbook."""


class VoiceAgent:
    """Main voice agent that processes queries and returns spoken responses."""

    def __init__(self, api_key: Optional[str] = None, provider: str = "groq"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.provider = provider
        self.conversation_history: List[Dict[str, str]] = []
        self.language_hint: Optional[str] = None

    def set_language(self, lang_code: str):
        """Set preferred language from voice detection."""
        self.language_hint = lang_code

    def process_text(self, user_text: str) -> str:
        """Process text input and return text response optimized for TTS."""
        try:
            import openai
        except ImportError:
            return "System error. Please install openai package."

        is_groq = self.provider == "groq" or "groq" in os.getenv("GROQ_API_KEY", "").lower()

        client = openai.OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1" if is_groq else None,
        )

        # Add language context if detected
        lang_context = ""
        if self.language_hint:
            lang_names = {
                "hi": "Hindi", "bn": "Bengali", "ta": "Tamil", "te": "Telugu",
                "mr": "Marathi", "gu": "Gujarati", "kn": "Kannada", "ml": "Malayalam",
                "pa": "Punjabi", "or": "Odia", "en": "English",
            }
            lang_name = lang_names.get(self.language_hint, self.language_hint)
            lang_context = f"\nThe user is speaking in {lang_name}. Respond ONLY in {lang_name}."

        system_msg = SYSTEM_PROMPT + lang_context

        messages = [{"role": "system", "content": system_msg}]
        messages.extend(self.conversation_history[-8:])  # Keep last 8 exchanges
        messages.append({"role": "user", "content": user_text})

        try:
            model = "llama-3.3-70b-versatile" if is_groq else "gpt-4o-mini"

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=get_tools(),
                tool_choice="auto",
                temperature=0.6,
                max_tokens=300,  # Short for voice
            )

            assistant_msg = response.choices[0].message

            # Handle tool calls
            if assistant_msg.tool_calls:
                messages.append(assistant_msg)
                for tool_call in assistant_msg.tool_calls:
                    result = execute_tool(
                        tool_call.function.name,
                        json.loads(tool_call.function.arguments),
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    })

                final = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.6,
                    max_tokens=300,
                )
                answer = final.choices[0].message.content
            else:
                answer = assistant_msg.content

            # Update history
            self.conversation_history.append({"role": "user", "content": user_text})
            self.conversation_history.append({"role": "assistant", "content": answer})

            return answer or "I didn't understand. Can you say that again?"

        except Exception as e:
            return f"There was a problem. Please try again. Error: {str(e)}"

    def reset(self):
        """Reset conversation."""
        self.conversation_history = []
        self.language_hint = None
