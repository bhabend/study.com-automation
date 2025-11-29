from app.llm_client import generate_text
from pathlib import Path
import os

PROMPTS_DIR = Path("config/prompts")

def load_prompt(name):
    p = PROMPTS_DIR / name
    return p.read_text(encoding="utf-8")

def generate_rewrite(extracted_struct):
    prompt = load_prompt("rewrite_prompt.txt")
    # include structured context + text for Gemini
    payload = prompt + "\n\n" + "PAGE TEXT:\n" + extracted_struct.get("text","")
    return generate_text(payload, model=os.getenv("GEMINI_MODEL"))

def generate_salary(degree_name):
    prompt = load_prompt("salary_prompt.txt") + f"\nDegree: {degree_name}"
    raw = generate_text(prompt, model=os.getenv("GEMINI_MODEL"))
    # expect JSON string - attempt to parse
    import json
    try:
        return json.loads(raw)
    except Exception:
        return {"salary_value": "", "salary_source": ""}
    
def apply_llm_citation(content):
    prompt = load_prompt("llm_citation_prompt.txt") + "\n\n" + content
    return generate_text(prompt, model=os.getenv("GEMINI_MODEL"))
