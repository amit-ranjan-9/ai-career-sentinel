import httpx
from bs4 import BeautifulSoup

def fetch_full_jd(url: str) -> str:
    """
    MCP Fetch Tool — fetches full job description from apply link
    Replaces the 500 char JSearch snippet with actual full JD content
    """
    if not url:
        return ""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove noise
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        # Return first 1500 chars — enough for LLM context
        return text[:1500]

    except Exception as e:
        print(f"[Fetch MCP] Could not fetch {url}: {e}")
        return ""