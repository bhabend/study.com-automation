import os
from serpapi import GoogleSearch

def get_competitors_and_gap(query, num=5):
    """
    Uses SerpAPI to find top competitor pages for a query and returns top N.
    Requires SERPAPI_KEY env var.
    """
    key = os.getenv("SERPAPI_KEY")
    if not key:
        return []
    params = {"engine": "google", "q": query, "api_key": key, "num": num}
    search = GoogleSearch(params)
    results = search.get_dict()
    organic = results.get("organic_results", [])
    return [{"title": r.get("title"), "link": r.get("link")} for r in organic[:num]]
