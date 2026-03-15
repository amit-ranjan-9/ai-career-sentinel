import httpx
import os
from dotenv import load_dotenv

load_dotenv()

JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY")

def search_jobs(query: str = "AI ML Python GenAI", location: str = "India") -> list:
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {
        "query": f"{query} in {location}",
        "page": "1",
        "num_pages": "2",
        "date_posted": "week"
    }
    try:
        response = httpx.get(url, headers=headers, params=params, timeout=40)
        data = response.json()
        jobs = []
        for job in data.get("data", []):
            city = job.get("job_city") or ""
            country = job.get("job_country") or ""
            location_str = ", ".join(filter(None, [city, country]))
            jobs.append({
                "title": job.get("job_title", ""),
                "company": job.get("employer_name", ""),
                "location": location_str or "India",
                "description": (job.get("job_description") or "")[:500],
                "apply_link": job.get("job_apply_link", ""),
                "posted": job.get("job_posted_at_datetime_utc", "")
            })
        return jobs
    except Exception as e:
        print(f"[JSearch Error] {e}")
        return []