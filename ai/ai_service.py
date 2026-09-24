"""AI Service abstraction layer.
Connects to Google Gemini API when configured, or provides seamless
offline AI fallback capabilities when API keys are absent or network fails.
"""
import os
import json
import logging
from config import Config

logger = logging.getLogger(__name__)

# Try importing google.generativeai safely
try:
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import google.generativeai as genai
    _GENAI_AVAILABLE = True
except ImportError:
    _GENAI_AVAILABLE = False


class AIService:
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.model_name = Config.GEMINI_MODEL
        self.is_demo_mode = Config.DEMO_MODE or not self.api_key
        self._model = None

        if not self.is_demo_mode and _GENAI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self._model = genai.GenerativeModel(self.model_name)
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini model: {e}. Falling back to Demo Mode.")
                self.is_demo_mode = True

    def get_status(self):
        """Returns the current AI operational status for UI display."""
        if not self.is_demo_mode and self._model:
            return {
                "mode": "live",
                "provider": "Google Gemini",
                "model": self.model_name,
                "label": "AI Engine: Google Gemini Active",
                "badge_class": "badge-success",
            }
        return {
            "mode": "demo",
            "provider": "Local Intelligent Fallback Engine",
            "model": "Rule-Based NLP & Question Bank",
            "label": "Demo Mode: Offline Question Bank & Rubric Evaluator",
            "badge_class": "badge-warning",
        }

    def generate_text(self, prompt, temperature=0.7):
        """Generates text from prompt using Gemini if available, else returns None."""
        if self.is_demo_mode or not self._model:
            return None

        try:
            response = self._model.generate_content(
                prompt,
                generation_config={"temperature": temperature}
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini generation call failed: {e}. Falling back.")
        return None

    def generate_json(self, prompt):
        """Generates structured JSON output from Gemini, stripping markdown fences."""
        raw = self.generate_text(prompt)
        if not raw:
            return None

        clean = raw.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        elif clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        clean = clean.strip()

        try:
            return json.loads(clean)
        except Exception as e:
            logger.warning(f"Failed to parse JSON from AI response: {e}")
            return None


ai_service = AIService()
