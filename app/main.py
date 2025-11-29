from app.google_sheet import GoogleSheet
from app.scraper import fetch_and_parse
from app.parser import extract_content
from app.scoring import score_page
from app.content_generator import generate_rewrite, generate_salary, apply_llm_citation
from app.docs_export import save_docx, generate_diff
from app.utils import log
import os

def process_row(row):
    degree = row.get("degree")
    url = row.get("url")
    log(f"Processing {degree} | {url}")

    soup = fetch_and_parse(url)
    parsed = extract_content(soup)
    score_before = score_page(parsed)

    rewritten = generate_rewrite(parsed)
    salary = generate_salary(degree)
    rewritten = rewritten.replace("{{SALARY_SOURCE}}", salary.get("salary_source", ""))
    rewritten = rewritten.replace("{{SALARY_VALUE}}", salary.get("salary_value", ""))

    final = apply_llm_citation(rewritten)
    # docs
    out_folder = "outputs"
    os.makedirs(out_folder, exist_ok=True)
    save_docx(f"{out_folder}/{degree}_original.docx", degree + " - original", parsed.get("text",""))
    save_docx(f"{out_folder}/{degree}_optimized.docx", degree + " - optimized", final)
    diff_text = generate_diff(parsed.get("text",""), final)
    with open(f"{out_folder}/{degree}_diff.txt", "w", encoding="utf-8") as f:
        f.write(diff_text)

    score_after = score_page({"text": final, "headings": parsed.get("headings",[]), "links": parsed.get("links",[])})
    return {"degree": degree, "final": final, "score_before": score_before, "score_after": score_after}

def main():
    sheet = GoogleSheet()
    rows = sheet.fetch_input_rows()
    outputs = []
    for row in rows:
        try:
            out = process_row(row)
            outputs.append({"degree": out["degree"], "final": out["final"]})
            log(f"Completed {out['degree']}")
        except Exception as e:
            log(f"Error processing {row.get('degree')}: {e}")
    sheet.push_output(outputs)
    log("All done.")

if __name__ == "__main__":
    main()
