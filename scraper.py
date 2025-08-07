import requests
from bs4 import BeautifulSoup
from typing import List

def search_duckduckgo(query: str, num_results: int = 3) -> List[str]:
    url = f"https://lite.duckduckgo.com/lite/?q={query}"
    try:
        res = requests.get(url, timeout=8)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = [a['href'] for a in soup.select('a') if 'http' in a.get('href', '')]
        return links[:num_results]
    except Exception as e:
        return []

def scrape_text_from_url(url: str) -> str:
    try:
        res = requests.get(url, timeout=8)
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        return ' '.join(paragraphs).strip()
    except Exception as e:
        return ""
