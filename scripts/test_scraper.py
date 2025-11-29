from app.scraper import fetch_and_parse
soup = fetch_and_parse("https://study.com/")
print(soup.title.string if soup.title else "No title")
