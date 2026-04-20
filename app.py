"""
Voice-First Accessibility Agent — Gradio UI
Voice in → Voice out. No reading or typing needed.
"""
import os
import gradio as gr
from agent.core import VoiceAgent
from voice.stt import transcribe_audio_bytes
from voice.tts import synthesize_speech

# Initialize agent
agent = None


def get_agent():
    global agent
    if agent is None:
        api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        agent = VoiceAgent(api_key=api_key, provider="groq")
    return agent


def process_voice(audio_path, api_key_input):
    """Process voice input: STT → Agent → TTS."""
    if not audio_path:
        return "No audio recorded.", None, None

    # Update API key if provided
    global agent
    if api_key_input and api_key_input.strip():
        agent = VoiceAgent(api_key=api_key_input.strip(), provider="groq")

    current_agent = get_agent()
    if not current_agent.api_key:
        return "⚠️ Please enter your Groq API key above. Get one free at console.groq.com", None, None

    # Read audio file
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    # STT
    stt_result = transcribe_audio_bytes(audio_bytes)
    if stt_result.get("error"):
        return f"❌ Could not understand audio: {stt_result['error']}", None, None

    user_text = stt_result.get("text", "")
    detected_lang = stt_result.get("language", "en")

    if not user_text:
        return "❌ No speech detected. Please try again.", None, None

    # Set language for agent
    current_agent.set_language(detected_lang)

    # Get response
    response_text = current_agent.process_text(user_text)

    # TTS
    audio_path = synthesize_speech(response_text, language=detected_lang, slow=False)

    # Format conversation
    conversation = f"🎤 **You ({detected_lang}):** {user_text}\n\n🔊 **Sahayak:** {response_text}"

    return conversation, audio_path, user_text


def process_text(text_input, api_key_input):
    """Process text input (fallback for typing)."""
    if not text_input or not text_input.strip():
        return "Please type something.", None, None

    global agent
    if api_key_input and api_key_input.strip():
        agent = VoiceAgent(api_key=api_key_input.strip(), provider="groq")

    current_agent = get_agent()
    if not current_agent.api_key:
        return "⚠️ Please enter your Groq API key above.", None, None

    response_text = current_agent.process_text(text_input.strip())
    audio_path = synthesize_speech(response_text, language="hi", slow=False)

    conversation = f"🎤 **You:** {text_input}\n\n🔊 **Sahayak:** {response_text}"
    return conversation, audio_path, text_input


def reset_conversation():
    """Reset the agent conversation."""
    global agent
    if agent:
        agent.reset()
    return "", None, "Conversation reset. नई बातचीत शुरू करें।"


# Build Gradio UI
with gr.Blocks(
    title="🔊 Sahayak — Voice Assistant for Rural India",
    theme=gr.themes.Soft(),
    css="""
    .main-header { text-align: center; margin-bottom: 1rem; }
    .emergency { background: #ffebee; border-radius: 10px; padding: 1rem; text-align: center; margin-bottom: 1rem; }
    """,
) as demo:

    gr.HTML("""
    <div class="emergency">
        🚨 <b>Emergency?</b> Say "Call ambulance" or "बुलाओ एम्बुलेंस" — or call <b>108</b> directly!
    </div>
    <div class="main-header">
        <h1>🔊 Sahayak — आवाज़ से बात करें</h1>
        <p>Voice assistant for farming, health, schemes & emergencies. Speak in any Indian language.</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            api_key = gr.Textbox(
                label="🔑 Groq API Key",
                type="password",
                placeholder="gsk_...",
                info="Free at console.groq.com — no credit card needed",
            )

            gr.HTML("<h3>🎤 Speak Your Question</h3>")
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Press record and speak",
            )

            gr.HTML("<h3>⌨️ Or Type (fallback)</h3>")
            text_input = gr.Textbox(
                label="Type your question",
                placeholder="गेहूं की बुवाई कब करें? / When to sow wheat?",
                lines=2,
            )

            with gr.Row():
                voice_btn = gr.Button("🎤 Process Voice", variant="primary", size="lg")
                text_btn = gr.Button("💬 Send Text", variant="secondary")
                reset_btn = gr.Button("🔄 Reset", variant="stop")

        with gr.Column(scale=2):
            gr.HTML("<h3>🔊 Response</h3>")
            response_box = gr.Markdown(label="Sahayak says...", value="Ask me anything! मुझसे कुछ भी पूछें!")
            audio_output = gr.Audio(label="🔊 Voice Response", type="filepath", autoplay=True)
            last_query = gr.Textbox(label="Last query", visible=False)

    # Examples
    gr.HTML("<h3>💡 Try saying:</h3>")
    with gr.Row():
        gr.Examples(
            examples=[
                ["गेहूं की बुवाई कब करें?"],
                ["बुखार आ रहा है क्या करूं"],
                ["एम्बुलेंस बुलाओ"],
                ["Kisan Credit Card kaise banwayen"],
                ["When to sow rice in Punjab?"],
                ["बाजार में प्याज का भाव क्या है"],
                ["Ladakh में nearest hospital"],
                ["Ayushman card kaise milega"],
            ],
            inputs=[text_input],
        )

    # Event handlers
    voice_btn.click(
        fn=process_voice,
        inputs=[audio_input, api_key],
        outputs=[response_box, audio_output, last_query],
    )

    text_btn.click(
        fn=process_text,
        inputs=[text_input, api_key],
        outputs=[response_box, audio_output, last_query],
    )

    text_input.submit(
        fn=process_text,
        inputs=[text_input, api_key],
        outputs=[response_box, audio_output, last_query],
    )

    reset_btn.click(
        fn=reset_conversation,
        outputs=[response_box, audio_output, last_query],
    )

    gr.HTML("""
    <div style="text-align: center; margin-top: 2rem; color: #666; font-size: 0.9rem;">
        <p>⚠️ This is an AI assistant, not a doctor or expert. For emergencies, call 108.</p>
        <p>Built for <b>GSSoC 2026</b> — Agents for India Track | By <a href="https://github.com/nawangdorjay">Nawang Dorjay</a></p>
    </div>
    """)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
