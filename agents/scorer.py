from groq import Groq
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

RESUME_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "resume.txt")

def load_resume() -> str:
    with open(RESUME_PATH, "r", encoding="utf-8") as f:
        return f.read()

def score_job_with_groq(job: dict) -> dict:
    resume = load_resume()
    prompt = f"""You are an expert career coach and AI recruiter.

Here is a candidate's resume:
{resume[:1500]}

Here is a job posting:
Title: {job['title']}
Company: {job['company']}
Location: {job['location']}
Description: {job['description']}
RAG Match Score: {job['match_score']}%

Respond in this exact format:
RATING: [GREEN/YELLOW/RED]
REASON: [One sentence why]
SKILL_GAP: [One skill they might be missing or 'None']
APPLY: [YES/MAYBE/NO]
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        job["claude_review"] = response.choices[0].message.content
    except Exception as e:
        print(f"[Scorer Error] {e}")
        job["claude_review"] = "RATING: YELLOW\nREASON: Could not score\nSKILL_GAP: None\nAPPLY: MAYBE"
    return job

def score_all_jobs(jobs: list) -> list:
    print("[Scorer] Groq/Llama is reviewing top jobs...")
    scored = []
    for job in jobs:
        reviewed = score_job_with_groq(job)
        scored.append(reviewed)
    return scored