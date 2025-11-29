from bs4 import BeautifulSoup

def extract_content(html_or_soup):
    """
    Accepts raw HTML string or a BeautifulSoup object.
    Returns a structured dictionary with headings, text, metadata, lists, and FAQs if available.
    """
    if not html_or_soup:
        return {}
    soup = html_or_soup if hasattr(html_or_soup, "find") else BeautifulSoup(html_or_soup, "html.parser")

    # Core article block detection
    article = soup.find("article") or soup.find("main") or soup

    title = (soup.find("title").get_text(strip=True) if soup.find("title") else "")
    meta_desc = ""
    md = soup.find("meta", {"name": "description"})
    if md and md.get("content"):
        meta_desc = md["content"]

    # headings and text
    headings = []
    for h in article.find_all(["h1", "h2", "h3"]):
        headings.append({"tag": h.name, "text": h.get_text(strip=True)})

    text = article.get_text("\n", strip=True)

    # links
    links = []
    for a in article.find_all("a", href=True):
        links.append({"href": a["href"], "text": a.get_text(strip=True)})

    # simple FAQ extraction by finding schema or Q/A style blocks (best-effort)
    faqs = []
    for q in article.select("[itemtype*='FAQPage'] [itemprop='mainEntity']"):
        # best-effort parse
        qtext = q.find(attrs={"itemprop":"name"})
        atext = q.find(attrs={"itemprop":"acceptedAnswer"})
        if qtext and atext:
            faqs.append({"q": qtext.get_text(strip=True), "a": atext.get_text(strip=True)})

    return {
        "title": title,
        "meta_description": meta_desc,
        "headings": headings,
        "text": text,
        "links": links,
        "faqs": faqs
    }
