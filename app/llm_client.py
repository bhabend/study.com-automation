"""
Unified Gemini Client (2025)
Supports:
- API Key (preferred)
- Service Account JSON (optional)
Uses new Gemini API (google.generativeai)
"""

import os
import json
import google.generativeai as genai
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from app.utils import log

# Default model
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def _configure_client():
    """
    Configure Gemini client. Supports:
    - GOOGLE_API_KEY
    - GOOGLE_SERVICE_ACCOUNT_JSON
    """

    api_key = os.getenv("GOOGLE_API_KEY")
    sa_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

    if api_key:
        genai.configure(api_key=api_key)
        log("Gemini client initialized with API KEY")
        return

    if sa_json:
        info = json.loads(sa_json)
        creds = service_account.Credentials.from_service_account_info(
            info,
            scopes=["https://www.googleapis.com/auth/generative-language"]
        )
        creds.refresh(Request())
        genai.configure(credentials=creds)
        log("Gemini client initialized with SERVICE ACCOUNT")
        return

    raise RuntimeError("❌ No Gemini credentials found. Set GOOGLE_API_KEY or GOOGLE_SERVICE_ACCOUNT_JSON.")


# Initialize on import
_configure_client()


def generate_text(prompt: str, model: str = None, temperature: float = 0.2):
    """
    Generate text using Gemini 1.5 API.
    Returns clean text string always.
    """

    model = model or DEFAULT_MODEL
    log(f"Calling Gemini model: {model}")

    try:
        model_client = genai.GenerativeModel(model)

        response = model_client.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 2048
            }
        )

        # Standardize text extraction
        if hasattr(response, "text"):
            return response.text.strip()

        return str(response)

    except Exception as e:
        log(f"Gemini API error: {e}")
        return f"[Error calling Gemini API: {str(e)}]"
