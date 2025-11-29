import os
from app.llm_client import run_gemini
from app.utils import load_prompt, log


def build_rewrite_payload(parsed):
    """
    Build a structured block of page content for the rewrite prompt.
    """
    title = parsed.get("title", "")
    headings = parsed.get("headings", [])
    text_blocks = parsed.get("text_blocks", [])
    metadata = parsed.get("metadata", {})
    links = parsed.get("links", [])

    parts = []

    parts.append(f"# TITLE\n{title}\n")
    parts.append("## HEADINGS\n" + "\n".join(headings) + "\n")
    parts.append("## TEXT BLOCKS\n" + "\n\n".join(text_blocks) + "\n")
    parts.append("## METADATA\n" + str(metadata) + "\n")
    parts.append("## LINKS\n" + "\n".join(links) + "\n")

    return "\n".join(parts)


def generate_rewrite(parsed):
    """
    Main rewrite engine for the Study.com automation.
    Uses the rewrite_page.txt template under /config/prompts.
    """
    prompt_template = load_prompt("rewrite_page.txt")
    if not prompt_template:
        raise Exception("rewrite_page.txt missing from config/prompts")

    log("Loaded rewrite prompt template.")

    payload_text = build_rewrite_payload(parsed)

    final_prompt = prompt_template.replace("{{PAGE_DATA}}", payload_text)

    log("Sending rewrite request to Gemini...")

    rewritten_text = run_gemini(final_prompt)

    log("Rewrite completed.")

    return rewritten_text
