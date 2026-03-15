# import sqlite3
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from mcp_tools.jsearch import search_jobs

# DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "seen_jobs.db")

# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS seen_jobs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             apply_link TEXT UNIQUE,
#             title TEXT,
#             company TEXT,
#             seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#     """)
#     conn.commit()
#     conn.close()

# def is_seen(apply_link: str) -> bool:
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT 1 FROM seen_jobs WHERE apply_link = ?", (apply_link,))
#     result = cursor.fetchone()
#     conn.close()
#     return result is not None

# def mark_seen(job: dict):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO seen_jobs (apply_link, title, company) VALUES (?, ?, ?)",
#             (job["apply_link"], job["title"], job["company"])
#         )
#         conn.commit()
#     except sqlite3.IntegrityError:
#         pass
#     conn.close()

# # def scrape_fresh_jobs() -> list:
# #     print("[Scraper] Fetching fresh jobs...")
# #     init_db()
# #     queries = [
# #         "Generative AI Engineer",
# #         "LLM Engineer Python",
# #         "AI ML Engineer",
# #         "NLP Engineer Python"
# #     ]
# #     all_jobs = []
# #     for query in queries:
# #         jobs = search_jobs(query=query, location="India")
# #         all_jobs.extend(jobs)

# #     fresh_jobs = []
# #     for job in all_jobs:
# #         if job["apply_link"] and not is_seen(job["apply_link"]):
# #             mark_seen(job)
# #             fresh_jobs.append(job)

# #     print(f"[Scraper] Found {len(fresh_jobs)} fresh jobs")
# #     return fresh_jobs
# def scrape_fresh_jobs() -> list:
#     print("[Scraper] Fetching fresh jobs...")
#     init_db()
#     queries = [
#         "Generative AI Engineer Bangalore",
#         "LLM Engineer Python Bangalore",
#         "AI ML Engineer Bangalore",
#         "NLP Engineer Python Bangalore"
#     ]
#     all_jobs = []
#     for query in queries:
#         jobs = search_jobs(query=query, location="Bangalore India")
#         all_jobs.extend(jobs)

#     fresh_jobs = []
#     for job in all_jobs:
#         if job["apply_link"] and not is_seen(job["apply_link"]):
#             mark_seen(job)
#             fresh_jobs.append(job)

#     print(f"[Scraper] Found {len(fresh_jobs)} fresh jobs")
#     return fresh_jobs



import sqlite3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_tools.jsearch import search_jobs
#from mcp_tools.fetch_mcp import fetch_full_jd
from mcp_tools.mcp_client import fetch_job_description_mcp

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "seen_jobs.db"
)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seen_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            apply_link TEXT UNIQUE,
            title TEXT,
            company TEXT,
            seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def is_seen(apply_link: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM seen_jobs WHERE apply_link = ?", (apply_link,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_seen(job: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO seen_jobs (apply_link, title, company) VALUES (?, ?, ?)",
            (job["apply_link"], job["title"], job["company"])
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

# def scrape_fresh_jobs() -> list:
#     print("[Scraper] Fetching fresh jobs...")
#     init_db()
#     queries = [
#         "Generative AI Engineer Bangalore",
#         "LLM Engineer Python Bangalore",
#         "AI ML Engineer Bangalore",
#         "NLP Engineer Python Bangalore"
#     ]
#     all_jobs = []
#     for query in queries:
#         jobs = search_jobs(query=query, location="Bangalore India")
#         all_jobs.extend(jobs)

#     fresh_jobs = []
#     for job in all_jobs:
#         if job["apply_link"] and not is_seen(job["apply_link"]):
#             mark_seen(job)

#             # MCP Fetch — get full JD instead of 500 char snippet
#             print(f"[Fetch MCP] Fetching full JD for: {job['title']} at {job['company']}")
#             #full_jd = fetch_full_jd(job["apply_link"])
#             full_jd = fetch_job_description_mcp(job["apply_link"])
#             if full_jd:
#                 job["description"] = full_jd
#             fresh_jobs.append(job)

#     print(f"[Scraper] Found {len(fresh_jobs)} fresh jobs with full JDs")
#     return fresh_jobs
def scrape_fresh_jobs() -> list:
    print("[Scraper] Fetching fresh jobs...")
    init_db()
    queries = [
        "Generative AI Engineer Python Bangalore",
        "LLM Engineer Python Bangalore",
        "AI ML Engineer Python Bangalore",
        "Agentic AI Developer Python Bangalore",
        "RAG Engineer LLM Bangalore",
        "NLP Engineer Python LLM Bangalore"
    ]

    # Keywords that MUST appear in title for relevance
    ALLOWED_TITLE_KEYWORDS = [
        "ai", "ml", "machine learning", "generative", "genai",
        "llm", "nlp", "python", "data science", "deep learning",
        "agentic", "rag", "engineer", "developer", "scientist"
    ]

    # Keywords that should be REJECTED from title
    BLOCKED_TITLE_KEYWORDS = [
        "product lead", "product manager", "devops", "asic",
        "digital design", "hardware", "vlsi", "frontend",
        "sales", "marketing", "hr", "finance", "computer vision",
        "principal engineer non-ai", "digital commerce"
    ]

    all_jobs = []
    for query in queries:
        jobs = search_jobs(query=query, location="Bangalore India")
        all_jobs.extend(jobs)

    fresh_jobs = []
    for job in all_jobs:
        if not job["apply_link"]:
            continue

        title_lower = job["title"].lower()

        # Block irrelevant titles
        if any(blocked in title_lower for blocked in BLOCKED_TITLE_KEYWORDS):
            print(f"[Scraper] Skipping irrelevant job: {job['title']}")
            continue

        # Only allow relevant titles
        if not any(allowed in title_lower for allowed in ALLOWED_TITLE_KEYWORDS):
            print(f"[Scraper] Skipping non-relevant job: {job['title']}")
            continue

        if not is_seen(job["apply_link"]):
            mark_seen(job)
            print(f"[Fetch MCP] Fetching full JD for: {job['title']} at {job['company']}")
            full_jd = fetch_job_description_mcp(job["apply_link"])
            if full_jd:
                job["description"] = full_jd
            fresh_jobs.append(job)

    print(f"[Scraper] Found {len(fresh_jobs)} relevant fresh jobs")
    return fresh_jobs