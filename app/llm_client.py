"""
Gemini client wrapper using google-auth AuthorizedSession.
This wrapper posts to the Google Generative API endpoint.
Requires GOOGLE_SERVICE_ACCOUNT_JSON to be set (service account with
Cloud Generative API and Sheets access), or ADC available in environment.
"""

import os
import json
import google.auth
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
from app.utils import log

# Default model; can be overridden by env GEMINI_MODEL
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", os.getenv("GEMINI_MODEL", "models/text-bison-001"))

def _get_authed_session():
    # If a service account JSON string is provided via env, use it.
    sa_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        info = json.loads(sa_json)
        creds = service_account.Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/cloud-platform"])
    else:
        creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    authed_session = AuthorizedSession(creds)
    return authed_session

def generate_text(prompt: str, model: str = None, temperature: float = 0.2, max_output_tokens: int = 768):
    """
    Call the Generative API to generate text.
    Note: API surface (endpoint / request) may vary by Google release; this wrapper uses the
    /v1beta2/models/{model}:generateText endpoint format which is widely available.
    """
    model = model or DEFAULT_MODEL
    session = _get_authed_session()
    # Compose endpoint (v1beta2 used here)
    endpoint = f"https://generativelanguage.googleapis.com/v1beta2/{model}:generateText"
    body = {
        "prompt": {"text": prompt},
        "temperature": temperature,
        "maxOutputTokens": max_output_tokens
    }
    log(f"Calling Gemini model: {model}")
    resp = session.post(endpoint, json=body, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    # Response shape depends on API version. Try common keys.
    text = ""
    if "candidates" in data:
        text = data["candidates"][0].get("output", "")
    elif "output" in data:
        # some variants put `output` at top-level
        text = data["output"][0].get("content", "")
    elif "results" in data:
        # fallback for different shapes
        results = data["results"]
        if results and "content" in results[0]:
            text = results[0]["content"]
    else:
        # best-effort: dump JSON if unexpected
        text = json.dumps(data)
    return text
