import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.embedder import embed_text, cosine_similarity

RESUME_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "resume.txt")

def load_resume() -> str:
    with open(RESUME_PATH, "r", encoding="utf-8") as f:
        return f.read()

def match_jobs_to_resume(jobs: list) -> list:
    print("[RAG Matcher] Scoring jobs against resume...")
    resume_text = load_resume()
    resume_vec = embed_text(resume_text)

    scored_jobs = []
    for job in jobs:
        jd_text = f"{job['title']} {job['company']} {job['description']}"
        jd_vec = embed_text(jd_text)
        score = cosine_similarity(resume_vec, jd_vec)
        job["match_score"] = round(score * 100, 2)
        scored_jobs.append(job)

    scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    top_jobs = scored_jobs[:5]
    print(f"[RAG Matcher] Top match: {top_jobs[0]['title']} at {top_jobs[0]['company']} — {top_jobs[0]['match_score']}%")
    return top_jobs