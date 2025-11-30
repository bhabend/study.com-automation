import os
import json
from utils import fetch_page, parse_content, save_json, load_json, simple_score, generate_diff

# Paths
BASE_DIR = os.path.dirname(__file__)
BEFORE_DIR = os.path.join(BASE_DIR, 'before_content')
AFTER_DIR = os.path.join(BASE_DIR, 'after_content')
DIFF_DIR = os.path.join(BASE_DIR, 'diffs')

# Ensure folders exist
os.makedirs(BEFORE_DIR, exist_ok=True)
os.makedirs(AFTER_DIR, exist_ok=True)
os.makedirs(DIFF_DIR, exist_ok=True)

# Load pages
with open(os.path.join(BASE_DIR, 'pages.json'), 'r', encoding='utf-8') as f:
    pages = json.load(f)['pages']

for page in pages:
    name = page['name']
    url = page['url']
    file_key = name.lower().replace(' ', '_')

    print(f"\n=== Processing: {name} ===")
    
    # Step 2: Fetch & parse content
    html = fetch_page(url)
    before_content = parse_content(html)
    save_json(os.path.join(BEFORE_DIR, f"{file_key}.json"), before_content)
    
    # Step 3: Score original content
    before_score = simple_score(before_content)
    print("Before Score:", before_score)
    
    # Step 4: LLM Rewrite simulation (manual rules applied)
    # For demo, we simulate improvement
    after_content = before_content.copy()
    after_content['headings'] = ['LLM-Optimized ' + h for h in after_content['headings']]
    after_content['paragraphs'] = [p + ' [Optimized]' for p in after_content['paragraphs']]
    after_content['lists'] = [lst + ['[Added LLM Table / Summary]'] for lst in after_content['lists']]
    save_json(os.path.join(AFTER_DIR, f"{file_key}.json"), after_content)
    
    # Step 7: Score after content
    after_score = simple_score(after_content)
    print("After Score:", after_score)
    
    # Step 8: Generate diff
    diff_text = generate_diff(before_content, after_content)
    with open(os.path.join(DIFF_DIR, f"{file_key}_diff.txt"), 'w', encoding='utf-8') as f:
        f.write(diff_text)
    print(f"Diff saved: diffs/{file_key}_diff.txt")

print("\nDemo complete! All steps simulated for 3 pages.")
