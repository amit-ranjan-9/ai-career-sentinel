from groq import Groq
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def write_morning_brief(jobs: list) -> str:
    print("[Brief Writer] Groq/Llama is writing your morning brief...")
    today = date.today().strftime("%d %B %Y")

    jobs_text = ""
    for i, job in enumerate(jobs, 1):
        jobs_text += f"""
Job {i}:
Title: {job['title']}
Company: {job['company']}
Location: {job['location']}
Match Score: {job['match_score']}%
Review: {job.get('claude_review', 'N/A')}
Apply Link: {job['apply_link']}
"""

    prompt = f"""You are a career assistant writing a daily job search brief.

Today is {today}. Here are the top matched jobs for a senior AI/ML engineer based in Bengaluru:
{jobs_text}

Write a clean morning brief. Rules:
- No emojis, no special symbols, no markdown, no bullet points with symbols
- Use plain text only
- Format each job exactly like this:

---
Job Title: [title]
Company: [company]
Location: [location]
Match Score: [score]%
Why it fits: [one line reason based on review]
Apply: [link]
---

Start with: "Good Morning - AI Career Sentinel Daily Brief - {today}"
End with one plain motivating line.
Keep it under 400 words. Professional and clean.
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[Brief Writer Error] {e}")
        return "Could not generate brief today. Check logs."