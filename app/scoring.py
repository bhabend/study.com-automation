"""
Scoring engine per workflow doc (weighted categories).
Returns original score 0-100 and a breakdown.
"""

WEIGHTS = {
    "content_structure": 20,
    "internal_linking": 15,
    "semantic_coverage": 20,
    "llm_citation_patterns": 25,
    "backlink_signals": 10,
    "freshness": 5,
    "ux_technical": 5
}

def score_page(parsed):
    # parsed: dict from parser.extract_content
    score = 0
    breakdown = {}

    # Content structure: check for H1 + H2s + answer-first summary
    hs = parsed.get("headings", [])
    has_h1 = any(h["tag"] == "h1" for h in hs)
    has_h2 = any(h["tag"] == "h2" for h in hs)
    structure_pts = 0
    if has_h1 and has_h2:
        structure_pts = WEIGHTS["content_structure"]
    elif has_h1 or has_h2:
        structure_pts = int(WEIGHTS["content_structure"] * 0.6)
    breakdown["content_structure"] = structure_pts
    score += structure_pts

    # Internal linking: count internal-looking hrefs (heuristic)
    links = parsed.get("links", [])
    internal = sum(1 for l in links if l["href"].startswith("/") or "study.com" in l["href"])
    linking_pts = min(WEIGHTS["internal_linking"], int(internal * 2))
    breakdown["internal_linking"] = linking_pts
    score += linking_pts

    # Semantic coverage: wordcount heuristic (and faqs)
    wc = len(parsed.get("text","").split())
    semantic_pts = 0
    if wc > 800:
        semantic_pts = WEIGHTS["semantic_coverage"]
    elif wc > 400:
        semantic_pts = int(WEIGHTS["semantic_coverage"] * 0.6)
    if parsed.get("faqs"):
        semantic_pts = min(WEIGHTS["semantic_coverage"], semantic_pts + 5)
    breakdown["semantic_coverage"] = semantic_pts
    score += semantic_pts

    # LLM citation patterns: presence of numeric tables / lists / summary
    text = parsed.get("text","")
    patterns_pts = 0
    if any(x in text.lower() for x in ["average", "median", "salary", "table", "faq"]):
        patterns_pts = WEIGHTS["llm_citation_patterns"]
    breakdown["llm_citation_patterns"] = patterns_pts
    score += patterns_pts

    # Backlink signals, freshness, ux - placeholders (requires enrichment)
    breakdown["backlink_signals"] = 0
    breakdown["freshness"] = 0
    breakdown["ux_technical"] = 0

    return {"score": score, "breakdown": breakdown}
