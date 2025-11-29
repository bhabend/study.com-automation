import requests
from bs4 import BeautifulSoup
from app.utils import log
from time import sleep

def fetch_page(url, timeout=15, user_agent=None):
    log(f"Fetching: {url}")
    headers = {"User-Agent": user_agent or "Mozilla/5.0 (StudyBot)"}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    # polite pause (adjust if doing large batches; consider rate-limiting)
    sleep(0.2)
    return r.text

def fetch_and_parse(url, timeout=15, user_agent=None):
    html = fetch_page(url, timeout=timeout, user_agent=user_agent)
    soup = BeautifulSoup(html, "html.parser")
    return soup
