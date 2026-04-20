# 🔊 Sahayak — Voice-First Accessibility Agent

A voice assistant for rural India. Speak in Hindi, Tamil, Telugu, Bengali, or any Indian language. Get answers about farming, health, government schemes, and emergencies — **no reading or typing required**.

Built by [Nawang Dorjay](https://github.com/nawangdorjay) — from Ladakh, for **GSSoC 2026** (Agents for India Track).

---

## 🎯 Why Voice-First?

> 250 million+ Indians have limited literacy. They can't use text-based chatbots. But they can **speak**.

This agent is designed for:
- Farmers who want weather and crop advice by voice
- Villagers who need health guidance without reading
- Anyone who finds typing difficult or inconvenient
- Users in remote areas with limited connectivity

**The missing layer** that makes all AI agents accessible.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🎤 **Voice Input** | Speak naturally — agent understands Hindi, English, and 9 Indian languages |
| 🔊 **Voice Output** | Agent speaks back in your language |
| 🌾 **Farming** | Crop advice, weather, market prices, pest management |
| 💊 **Health** | Symptom guidance, nearest hospital, emergency numbers |
| 🏛️ **Schemes** | PM-KISAN, Ayushman Bharat, KCC, Ujjwala, PM Awas |
| 🚨 **Emergency** | Say "call ambulance" — get 108 immediately |
| ⏱️ **Short Responses** | Every answer under 30 seconds of speaking time |

---

## 🛠️ Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **STT** | OpenAI Whisper / Groq Whisper | Best multilingual support for Indic languages |
| **TTS** | Google TTS (gTTS) | Free, supports 10+ Indian languages |
| **LLM** | Llama 3.3 70B (Groq) / GPT-4o-mini | Fast, cheap, multilingual |
| **UI** | Gradio | Better voice/audio support than Streamlit |
| **Data** | JSON | Offline-capable, easy to update |

---

## 📦 Installation

```bash
# Clone
git clone https://github.com/nawangdorjay/voice-assistant-agent.git
cd voice-assistant-agent

# Install
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your free Groq API key from console.groq.com:
# GROQ_API_KEY=gsk_xxxxx

# Run
python app.py
```

Open `http://localhost:7860` in your browser.

---

## 📁 Project Structure

```
voice-assistant-agent/
├── app.py                      # Gradio voice UI
├── agent/
│   ├── __init__.py
│   ├── core.py                 # Agent logic (short, voice-optimized responses)
│   └── tools.py                # Unified tools (farming, health, schemes, etc.)
├── voice/
│   ├── __init__.py
│   ├── stt.py                  # Speech-to-Text (Whisper API)
│   └── tts.py                  # Text-to-Speech (gTTS)
├── data/
│   ├── crops_summary.json      # Quick crop data (10 crops)
│   ├── health_quick.json       # Health conditions (10 conditions)
│   ├── emergency.json          # Emergency numbers (12 states)
│   ├── schemes_quick.json      # Government schemes (8 schemes)
│   └── prices_quick.json       # Market prices (12 commodities)
├── tests/
│   └── test_tools.py           # 14 tool validation tests
├── .github/workflows/
│   └── ci.yml                  # GitHub Actions CI
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧪 Testing

```bash
python tests/test_tools.py
```

14 tests covering: crop advice, weather, health, emergency numbers, schemes, and market prices.

---

## 🗣️ Supported Languages

| Language | Voice Input | Voice Output |
|----------|------------|--------------|
| हिन्दी (Hindi) | ✅ Whisper | ✅ gTTS |
| English | ✅ Whisper | ✅ gTTS |
| தமிழ் (Tamil) | ✅ Whisper | ✅ gTTS |
| తెలుగు (Telugu) | ✅ Whisper | ✅ gTTS |
| বাংলা (Bengali) | ✅ Whisper | ✅ gTTS |
| मराठी (Marathi) | ✅ Whisper | ✅ gTTS |
| ગુજરાતી (Gujarati) | ✅ Whisper | ✅ gTTS |
| ಕನ್ನಡ (Kannada) | ✅ Whisper | ✅ gTTS |
| മലയാളം (Malayalam) | ✅ Whisper | ✅ gTTS |
| ਪੰਜਾਬੀ (Punjabi) | ✅ Whisper | ✅ gTTS |

---

## 💡 Example Interactions

| You say (in Hindi) | Sahayak responds |
|---------------------|------------------|
| "गेहूं की बुवाई कब करें?" | "गेहूं की बुवाई अक्टूबर से नवंबर के बीच करें। 15 नवंबर के बाद हर हफ्ते देरी से 50 किलो प्रति हेक्टेयर उपज कम होती है।" |
| "बुखार आ रहा है" | "आराम करें और खूब पानी पिएं। पैरासिटामोल 500 एमजी लें। अगर 3 दिन से ज्यादा बुखार हो तो डॉक्टर को दिखाएं।" |
| "एम्बुलेंस बुलाओ" | "एम्बुलेंस नंबर है एक शून्य आठ। अभी कॉल करें।" |
| "Kisan Credit Card kaise banwayen" | "किसान क्रेडिट कार्ड के लिए अपने नजदीकी बैंक में जाएं। जमीन के कागजात और आधार कार्ड ले जाएं। ब्याज दर सिर्फ 4% सालाना है।" |

---

## 🔮 Future Improvements

- [ ] Offline mode with Vosk (offline STT) for no-internet areas
- [ ] WhatsApp voice bot integration
- [ ] Wake word detection ("Hey Sahayak")
- [ ] Integration with existing farmer and health agents
- [ ] Regional accent support for better accuracy
- [ ] SMS fallback for feature phones

---

## ⚠️ Disclaimer

This is an AI assistant, not a medical professional or agricultural expert. For emergencies, call **108** (ambulance) or **112** (all emergencies) directly.

---

## 📄 License

MIT

---

## 👨‍💻 Author

**Nawang Dorjay** — B.Tech CSE (Data Science), MAIT Delhi
From Nubra Valley, Leh, Ladakh 🏔️

- [GitHub](https://github.com/nawangdorjay)
- [Email](mailto:nawangdorjay09@gmail.com)

Built for **GSSoC 2026** — Agents for India Track.
