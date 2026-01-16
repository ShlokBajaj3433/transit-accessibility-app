import json
import os
import re
from typing import Any, Dict, Optional

# If running code without the correct dependencies, it will not immediately fail
try:
    # Loads .env if present
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv is optional; if missing, env vars must already be set
    pass

try:
    # Gemini SDK (Google Gen AI)
    from google import genai
except Exception:
    genai = None


class ChatService:
    """
    Job 1: Synthesizer
      - Takes transit + climate + vision signals and asks Gemini to produce a helpful, friendly sentence.

    Job 2: Interpreter
      - Takes messy speech-to-text and asks Gemini to decode intended destination.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_id = os.getenv("GEMINI_MODEL_ID", "gemini-3-pro-preview").strip()

        self._client = None
        # Creates a client if the correct dependencies are installed and an api key is provided
        if genai is not None and self.api_key:
            self._client = genai.Client(api_key=self.api_key)

    # Synthesizer
    def synthesize(self, transit: str, climate: str, vision: str) -> str:
        """
        Produce a user-friendly sentence combining:
          - transit: e.g., "Bus 504, 15 mins"
          - climate: e.g., "0.4kg CO2 saved"
          - vision: e.g., "Ramp Detected: True"
        """
        transit = (transit or "").strip()
        climate = (climate or "").strip()
        vision = (vision or "").strip()

        # Simple message if Gemini isn't configured
        if not self._client:
            ramp = self._extract_ramp_bool(vision)
            ramp_msg = "has a wheelchair ramp available" if ramp is True else (
                "may not have a wheelchair ramp" if ramp is False else "ramp availability is unknown"
            )
            return f"Your trip update: {transit}. Accessibility: this vehicle {ramp_msg}. Climate impact: {climate}."

        # General rules for the Gemini prompt
        system_prompt = (
            "You are an accessibility-first transit assistant. "
            "Write 1–2 friendly, helpful sentences for a rider. "
            "Be concrete and encouraging. "
            "If ramp is detected true, explicitly mention wheelchair ramp availability. "
            "If ramp is false/unknown, phrase cautiously. "
            "If climate contains CO2 saved, you may add a simple, fun equivalence but do not invent extreme numbers. "
            "Do not output bullet points; output plain text."
        )

        # The actual inputs for the Gemini call
        user_prompt = f"""
Transit info: {transit}
Climate info: {climate}
Vision info: {vision}

Return a helpful message for the user.
""".strip()

        text = self._generate_text(system_prompt, user_prompt)
        return text or "Thanks! I couldn't generate a message right now, but your trip info is ready."

    # Backwards-compatible alias (in case main.py calls a different name)
    def get_chat_response(self, transit: str, climate: str, vision: str) -> str:
        return self.synthesize(transit=transit, climate=climate, vision=vision)

    # Interpreter
    def interpret_destination(self, messy_speech_text: str) -> str:
        """
        Convert messy speech-to-text (stutters, partial words) into a clean destination.
        Requires speech from user to already be converted to text
        Example input: "Un... un... onion... sta... shun."
        Example output: "Union Station"
        """
        raw = (messy_speech_text or "").strip()
        if not raw:
            return ""

        # Fallback if Gemini isn't configured
        if not self._client:
            return self._heuristic_destination(raw)

        # General rules for the Gemini prompt
        system_prompt = (
            "You decode messy speech-to-text into the intended transit destination. "
            "The user is likely trying to say a place name (station, mall, street, etc.). "
            "Return STRICT JSON only, matching this schema:\n"
            "{\n"
            '  "destination": string,\n'
            '  "confidence": number,\n'
            '  "notes": string\n'
            "}\n"
            "Confidence is 0 to 1. Keep notes short."
        )

        # The actual inputs for the Gemini call
        user_prompt = f"""
Messy speech-to-text:
{raw}

Decode the intended destination.
Return STRICT JSON only.
""".strip()

        text = self._generate_text(system_prompt, user_prompt)
        parsed = self._safe_parse_json(text)

        if isinstance(parsed, dict):
            dest = str(parsed.get("destination", "")).strip()
            if dest:
                return dest

        # If model didn't follow JSON, try a second-pass extraction
        dest = self._extract_destination_from_text(text)
        return dest or self._heuristic_destination(raw)

    # Backwards-compatible alias
    def interpret_speech(self, messy_speech_text: str) -> str:
        return self.interpret_destination(messy_speech_text)

    # Helper to generate Gemini calls
    def _generate_text(self, system_prompt: str, user_prompt: str) -> str:
        """
        Uses Gemini 3 API via google-genai SDK.
        Uses low thinking level for responsiveness.
        """
        try:
            # Gemini 3 docs recommend thinking_level for latency control.
            resp = self._client.models.generate_content(
                model=self.model_id,
                contents=[
                    {"role": "system", "parts": [{"text": system_prompt}]},
                    {"role": "user", "parts": [{"text": user_prompt}]},
                ],
                config={
                    "thinking_config": {"thinking_level": "low"},
                },
            )

            # Response text is typically in resp.text with google-genai
            out = getattr(resp, "text", None)
            if out:
                return out.strip()

            # Safety: attempt to reconstruct if needed
            return str(resp).strip()
        except Exception:
            return ""

    # Parsing text
    def _safe_parse_json(self, text: Optional[str]) -> Optional[Any]:
        if not text:
            return None
        text = text.strip()

        # If model wrapped JSON in code fences, strip them
        if text.startswith("```"):
            text = re.sub(r"^```[a-zA-Z]*\n", "", text)
            text = re.sub(r"\n```$", "", text).strip()

        try:
            return json.loads(text)
        except Exception:
            # Try to locate the first {...} block
            m = re.search(r"\{.*\}", text, flags=re.DOTALL)
            if m:
                try:
                    return json.loads(m.group(0))
                except Exception:
                    return None
        return None

    # Incase Gemini returns a call that doesn't conform to the exact specifications
    def _extract_destination_from_text(self, text: Optional[str]) -> str:
        if not text:
            return ""
        # Try common patterns like "Destination: Union Station"
        m = re.search(r"destination\s*[:\-]\s*(.+)", text, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip().strip('"').strip()

        # Otherwise, take first line and clean
        line = text.strip().splitlines()[0].strip()
        # Avoid returning JSON-like or empty
        if line.startswith("{") or line.startswith("["):
            return ""
        return line.strip(' "\'')

    # In case Gemini can't be used, attempts to get a usable result.
    def _heuristic_destination(self, raw: str) -> str:
        cleaned = raw

        # Remove ellipses-like repetitions and filler
        cleaned = re.sub(r"\b(um+|uh+)\b", " ", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"[.]{2,}", " ", cleaned)          # "..." -> space
        cleaned = re.sub(r"\b(\w+)\s*\.\.\s*\b", r"\1 ", cleaned)  # "sta... " -> "sta "
        cleaned = re.sub(r"[^a-zA-Z0-9\s\-']", " ", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        # Title-case as a best effort
        return cleaned.title()

    # In case Gemini can't be used, attempts to determine if a ramp is present
    def _extract_ramp_bool(self, vision: str) -> Optional[bool]:
        """
        Extract Ramp Detected: True/False from vision string.
        """
        if not vision:
            return None
        m = re.search(r"ramp\s*detected\s*[:=]\s*(true|false)", vision, flags=re.IGNORECASE)
        if not m:
            return None
        val = m.group(1).lower()
        return True if val == "true" else False
