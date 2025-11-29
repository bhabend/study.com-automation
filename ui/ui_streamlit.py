import streamlit as st
from app.scraper import fetch_and_parse
from app.parser import extract_content
from app.content_generator import generate_rewrite

st.title("Study.com Automation - Demo UI")

st.write("Paste URLs (one per line) or upload a .csv/.xlsx of URLs (demo mode).")

urls_text = st.text_area("URLs (one per line)")

if st.button("Process URLs (demo)"):
    urls = [u.strip() for u in urls_text.splitlines() if u.strip()]
    for u in urls:
        st.write(f"Fetching: {u}")
        soup = fetch_and_parse(u)
        parsed = extract_content(soup)
        st.write("Title:", parsed.get("title"))
        rewritten = generate_rewrite(parsed)
        st.text_area("Rewritten", value=rewritten, height=300)
