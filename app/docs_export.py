from docx import Document
import difflib
from app.utils import log

def save_docx(path, title, body_text):
    doc = Document()
    doc.add_heading(title, level=1)
    for p in body_text.split("\n"):
        doc.add_paragraph(p)
    doc.save(path)
    log(f"Saved docx: {path}")

def generate_diff(original_text, optimized_text):
    """
    Returns a simple unified diff string.
    """
    orig_lines = original_text.splitlines()
    opt_lines = optimized_text.splitlines()
    diff = difflib.unified_diff(orig_lines, opt_lines, fromfile='original', tofile='optimized', lineterm='')
    return "\n".join(diff)
