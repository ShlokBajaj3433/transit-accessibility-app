# backend/tests/test_chat_service.py
from backend.services.chat_service import ChatService

class _FakeResponse:
    def __init__(self, text: str):
        self.text = text

class _FakeModels:
    def __init__(self, text: str):
        self._text = text
        self.last_call = None  # capture args for assertions if you want

    def generate_content(self, model=None, contents=None, config=None):
        self.last_call = {"model": model, "contents": contents, "config": config}
        return _FakeResponse(self._text)


class _FakeClient:
    def __init__(self, text: str):
        self.models = _FakeModels(text)


def test_interpreter_empty_returns_empty():
    """
    Job 2 should not hallucinate a destination when the input is empty.
    """
    s = ChatService()
    # Force fallback path (no Gemini)
    s._client = None

    out = s.correct_speech_input("")
    assert out == ""


def test_interpreter_is_sensitive_to_input():
    """
    Job 2 should not always return the same destination.
    With fallback heuristics, at minimum it should reflect input text.
    """
    s = ChatService()
    s._client = None  # fallback

    out = s.correct_speech_input("metrotown")
    assert "metrotown" in out.lower()
    assert "union station" not in out.lower()


def test_interpreter_uses_gemini_json_when_available():
    """
    Job 2: If Gemini returns JSON with a destination, the service should return it.
    """
    s = ChatService()
    # Mock Gemini client response
    s._client = _FakeClient('{"destination":"Union Station","confidence":0.92,"notes":"best match"}')

    out = s.correct_speech_input("Un... un... onion... sta... shun.")
    assert out == "Union Station"


def test_synthesizer_fallback_includes_transit_climate_and_ramp():
    """
    Job 1 fallback should still combine the three inputs into a helpful message.
    We assert presence of key info (deterministic).
    """
    s = ChatService()
    s._client = None  # fallback

    transit = "Bus 504, 15 mins"
    climate = "0.4kg CO2 saved"
    vision = "Ramp Detected: True"

    out = s.get_chat_response(transit, climate, vision)

    # Must include transit details
    assert "504" in out
    assert "15" in out

    # Must mention climate info in some form
    assert "co2" in out.lower()
    assert "0.4" in out

    # Must mention ramp / wheelchair accessibility
    assert ("ramp" in out.lower()) or ("wheelchair" in out.lower())


def test_synthesizer_uses_gemini_text_when_available():
    """
    Job 1: If Gemini returns text, the service should return it (or a cleaned version).
    """
    s = ChatService()
    s._client = _FakeClient("Great news! The 504 arrives in 15 minutes and has a wheelchair ramp available.")

    out = s.get_chat_response("Bus 504, 15 mins", "0.4kg CO2 saved", "Ramp Detected: True")
    assert out.startswith("Great news!")
    assert "wheelchair" in out.lower()
