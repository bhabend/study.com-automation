import streamlit as st
import pandas as pd

from app.scraper import fetch_and_parse
from app.parser import extract_content
from app.content_generator import generate_rewrite
from app.scoring import score_rewrite
from app.docs_export import export_to_docx

st.set_page_config(page_title="Study.com Automation", layout="wide")
st.title("📘 Study.com Automation Dashboard")

st.write("Use this tool to scrape pages, extract content, rewrite using LLM, score the output, and export documents.")

# ------------------------------------------------------
# INPUT SECTION
# ------------------------------------------------------
st.header("1. Input URLs")

col1, col2 = st.columns(2)

with col1:
    urls_text = st.text_area("Paste URLs (one per line)", height=200)

with col2:
    uploaded_file = st.file_uploader("OR upload a file (.csv, .xlsx, .txt)")

def load_urls():
    """Loads URLs from text box or uploaded file."""
    if uploaded_file:
        ext = uploaded_file.name.split(".")[-1].lower()

        if ext == "csv":
            df = pd.read_csv(uploaded_file)
            return df.iloc[:, 0].dropna().tolist()

        elif ext == "xlsx":
            df = pd.read_excel(uploaded_file)
            return df.iloc[:, 0].dropna().tolist()

        elif ext == "txt":
            text = uploaded_file.read().decode("utf-8")
            return [line.strip() for line in text.splitlines() if line.strip()]

        else:
            st.error("Unsupported file type.")
            return []

    # fallback to textbox
    return [u.strip() for u in urls_text.splitlines() if u.strip()]


# ------------------------------------------------------
# PROCESSING SECTION
# ------------------------------------------------------
st.header("2. Process URLs")

if st.button("Run Automation"):
    urls = load_urls()

    if not urls:
        st.error("No URLs provided.")
        st.stop()

    st.success(f"Processing {len(urls)} URLs...")
    progress = st.progress(0)
    results = []

    for i, url in enumerate(urls, start=1):
        st.write(f"🔍 Fetching **{url}** ...")

        # SCRAPE
        soup = fetch_and_parse(url)

        # PARSE
        parsed = extract_content(soup)

        # REWRITE
        st.write("✍️ Rewriting with LLM ...")
        rewritten = generate_rewrite(parsed)

        # SCORE
        st.write("📊 Scoring rewrite ...")
        score = score_rewrite(rewritten)

        # EXPORT
        st.write("📄 Exporting DOCX ...")
        docx_path = export_to_docx(parsed, rewritten, url)

        results.append({
            "url": url,
            "title": parsed.get("title", ""),
            "rewrite": rewritten,
            "score": score,
            "docx_path": docx_path
        })

        progress.progress(i / len(urls))

    st.success("Automation complete!")

    # ------------------------------------------------------
    # RESULTS SECTION
    # ------------------------------------------------------
    st.header("3. Results")

    for res in results:
        with st.expander(res["title"] or res["url"]):
            st.write(f"**URL:** {res['url']}")
            st.write(f"**Score:** {res['score']} / 100")

            st.subheader("Rewritten Content")
            st.text_area("Output", value=res["rewrite"], height=300)

            if res["docx_path"]:
                with open(res["docx_path"], "rb") as f:
                    st.download_button(
                        label="⬇️ Download DOCX",
                        data=f,
                        file_name=res["docx_path"].split("/")[-1],
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
