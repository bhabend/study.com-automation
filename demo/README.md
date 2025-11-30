# Study.com Automation Demo

This demo simulates the **AI-assisted content optimization workflow** for 3 certification pages:

- Nursing Certification: https://nursing.study.com/
- Teaching License: https://teachinglicense.study.com/
- GRE / Graduate Exams: https://graduateexams.study.com/gre/

## Folder Structure
- `demo.py` — main script to run the demo
- `pages.json` — input URLs
- `before_content/` — original extracted page content
- `after_content/` — LLM-optimized content
- `diffs/` — side-by-side diffs showing changes
- `utils.py` — helper functions for fetching, parsing, scoring, diffing

## How to Run
1. Clone or navigate to this folder.
2. Install dependencies:
   ```bash
   pip install requests beautifulsoup4
