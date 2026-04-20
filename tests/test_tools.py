"""Tests for Voice Assistant Agent tools."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent.tools import execute_tool


def test_crop_rice():
    result = execute_tool("get_crop_advice", {"crop": "rice"})
    assert result["found"] is True
    assert result["crop"] == "rice"
    print("✅ test_crop_rice passed")


def test_crop_wheat():
    result = execute_tool("get_crop_advice", {"crop": "wheat"})
    assert result["found"] is True
    print("✅ test_crop_wheat passed")


def test_crop_fuzzy():
    result = execute_tool("get_crop_advice", {"crop": "sugar"})
    assert result["found"] is True
    print("✅ test_crop_fuzzy passed")


def test_crop_unknown():
    result = execute_tool("get_crop_advice", {"crop": "dragonfruit"})
    assert result["found"] is False
    print("✅ test_crop_unknown passed")


def test_weather():
    result = execute_tool("get_weather", {"location": "Leh"})
    assert "temperature" in result
    print("✅ test_weather passed")


def test_health_fever():
    result = execute_tool("get_health_advice", {"condition": "fever"})
    assert result["found"] is True
    assert "what_to_do" in result
    print("✅ test_health_fever passed")


def test_health_chest():
    result = execute_tool("get_health_advice", {"condition": "chest pain"})
    assert result["found"] is True
    print("✅ test_health_chest passed")


def test_emergency_national():
    result = execute_tool("get_emergency_number", {"service": "ambulance"})
    assert result["number"] == "108"
    print("✅ test_emergency_national passed")


def test_emergency_ladakh():
    result = execute_tool("get_emergency_number", {"service": "ambulance", "state": "ladakh"})
    assert result["number"] == "108"
    print("✅ test_emergency_ladakh passed")


def test_emergency_women():
    result = execute_tool("get_emergency_number", {"service": "women helpline"})
    assert result["number"] == "1091"
    print("✅ test_emergency_women passed")


def test_scheme_loan():
    result = execute_tool("get_scheme_info", {"query": "loan"})
    assert len(result["schemes"]) > 0
    print("✅ test_scheme_loan passed")


def test_scheme_insurance():
    result = execute_tool("get_scheme_info", {"query": "insurance"})
    assert len(result["schemes"]) > 0
    print("✅ test_scheme_insurance passed")


def test_price_rice():
    result = execute_tool("get_market_price", {"commodity": "rice"})
    assert result.get("price") is not None
    print("✅ test_price_rice passed")


def test_price_onion():
    result = execute_tool("get_market_price", {"commodity": "onion"})
    assert result.get("price") is not None
    print("✅ test_price_onion passed")


if __name__ == "__main__":
    tests = [
        test_crop_rice, test_crop_wheat, test_crop_fuzzy, test_crop_unknown,
        test_weather, test_health_fever, test_health_chest,
        test_emergency_national, test_emergency_ladakh, test_emergency_women,
        test_scheme_loan, test_scheme_insurance, test_price_rice, test_price_onion,
    ]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
    print(f"\n{'='*40}\nResults: {passed} passed, {failed} failed")
    if failed == 0:
        print("All tests passed! 🎉")
