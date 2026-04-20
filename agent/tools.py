"""
Voice Assistant Agent — Tool Functions
Unified tools covering farming, health, schemes, and general info.
"""
import json
import requests
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def _load_json(filename: str) -> dict:
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_tools():
    """Return tool definitions for function calling."""
    return [
        {
            "type": "function",
            "function": {
                "name": "get_crop_advice",
                "description": "Get farming advice about a specific crop.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "crop": {"type": "string", "description": "Crop name"},
                        "question": {"type": "string", "description": "What the farmer wants to know"}
                    },
                    "required": ["crop"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City or area name"}
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_health_advice",
                "description": "Get health advice for a symptom or condition.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "condition": {"type": "string", "description": "Symptom or health condition"}
                    },
                    "required": ["condition"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_emergency_number",
                "description": "Get emergency phone numbers for a state or service type.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service": {"type": "string", "description": "Service type: ambulance, police, fire, women helpline, etc."},
                        "state": {"type": "string", "description": "Indian state name"}
                    },
                    "required": ["service"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_scheme_info",
                "description": "Get information about a government scheme or benefit.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "What the person needs (loan, insurance, subsidy, etc.)"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_market_price",
                "description": "Get current market price for a crop or commodity.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commodity": {"type": "string", "description": "Crop or commodity name"}
                    },
                    "required": ["commodity"]
                }
            }
        },
    ]


def execute_tool(tool_name: str, arguments: dict) -> dict:
    """Execute a tool and return result."""
    handlers = {
        "get_crop_advice": _crop_advice,
        "get_weather": _weather,
        "get_health_advice": _health_advice,
        "get_emergency_number": _emergency_number,
        "get_scheme_info": _scheme_info,
        "get_market_price": _market_price,
    }
    handler = handlers.get(tool_name)
    if handler:
        return handler(**arguments)
    return {"error": f"Unknown tool: {tool_name}"}


def _crop_advice(crop: str, question: str = "") -> dict:
    """Get crop farming advice."""
    crops = _load_json("crops_summary.json")
    key = crop.lower().strip()

    if key in crops:
        return {"found": True, "crop": key, **crops[key]}

    for k in crops:
        if key in k or k in key:
            return {"found": True, "crop": k, **crops[k]}

    return {"found": False, "message": f"No data for {crop}. Try: rice, wheat, cotton, tomato, potato, onion, sugarcane, maize."}


def _weather(location: str) -> dict:
    """Get current weather."""
    try:
        resp = requests.get(
            f"https://wttr.in/{location}?format=j1",
            timeout=10,
            headers={"User-Agent": "VoiceAgent/1.0"},
        )
        if resp.status_code == 200:
            data = resp.json()
            current = data.get("current_condition", [{}])[0]
            return {
                "location": location,
                "temperature": current.get("temp_C", "?"),
                "humidity": current.get("humidity", "?"),
                "condition": current.get("weatherDesc", [{}])[0].get("value", "Unknown"),
                "wind_speed": current.get("windspeedKmph", "?"),
            }
    except Exception:
        pass
    return {"error": f"Could not get weather for {location}"}


def _health_advice(condition: str) -> dict:
    """Get basic health advice."""
    conditions = _load_json("health_quick.json")
    key = condition.lower().strip()

    if key in conditions:
        return {"found": True, **conditions[key]}

    for k in conditions:
        if key in k or k in key:
            return {"found": True, **conditions[k]}

    return {
        "found": False,
        "message": "For any health problem, visit your nearest PHC or call 108 for ambulance.",
    }


def _emergency_number(service: str, state: str = "") -> dict:
    """Get emergency numbers."""
    contacts = _load_json("emergency.json")
    service_lower = service.lower().strip()

    # National defaults
    national = contacts.get("national", {})
    number = national.get(service_lower, national.get("emergency", "112"))

    # State-specific if available
    if state:
        state_lower = state.lower().strip()
        if state_lower in contacts:
            state_data = contacts[state_lower]
            if service_lower in state_data:
                number = state_data[service_lower]

    return {"service": service, "state": state or "national", "number": number}


def _scheme_info(query: str) -> dict:
    """Get government scheme info."""
    schemes = _load_json("schemes_quick.json")
    query_lower = query.lower()

    matched = []
    for scheme in schemes:
        keywords = scheme.get("keywords", [])
        if any(query_lower in kw for kw in keywords) or query_lower in scheme.get("name", "").lower():
            matched.append(scheme)

    if not matched:
        matched = schemes[:3]  # Return top 3 as fallback

    return {"query": query, "schemes": matched[:3]}


def _market_price(commodity: str) -> dict:
    """Get market price."""
    prices = _load_json("prices_quick.json")
    key = commodity.lower().strip()

    if key in prices:
        return {"commodity": key, **prices[key]}

    for k in prices:
        if key in k or k in key:
            return {"commodity": k, **prices[k]}

    return {"found": False, "message": f"No price data for {commodity}. Check your local mandi."}
