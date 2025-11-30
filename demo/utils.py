import requests
from bs4 import BeautifulSoup
import json
import difflib

def fetch_page(url):
    """Fetch HTML content of a page."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch {url}")

def parse_content(html):
    """Extract headings, paragraphs, and lists from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])]
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
    lists = []
    for ul in soup.find_all('ul'):
        items = [li.get_text(strip=True) for li in ul.find_all('li')]
        if items:
            lists.append(items)
    return {
        "headings": headings,
        "paragraphs": paragraphs,
        "lists": lists
    }

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def simple_score(content):
    """Simplified scoring: Structure + Semantics + Internal Links + LLM Patterns."""
    structure = min(len(content['headings']) * 2, 20)
    semantics = min(len(content['paragraphs']) // 2, 20)
    internal_links = min(len([p for p in content['paragraphs'] if 'study.com' in p]) * 3, 15)
    llm_patterns = min(len(content['lists']) * 8, 25)
    total = structure + semantics + internal_links + llm_patterns
    return {
        "Structure": structure,
        "Semantics": semantics,
        "Internal Links": internal_links,
        "LLM Patterns": llm_patterns,
        "Total": total
    }

def generate_diff(before, after):
    """Generate a simple line-based diff."""
    before_text = json.dumps(before, indent=2, ensure_ascii=False).splitlines()
    after_text = json.dumps(after, indent=2, ensure_ascii=False).splitlines()
    diff = difflib.unified_diff(before_text, after_text, lineterm='')
    return '\n'.join(diff)
