import os
from datetime import date

REPORTS_DIR = r"C:\Users\amitr\OneDrive\Desktop\job_search_agent\data\reports"

def save_daily_report(brief: str) -> str:
    if not os.path.exists(REPORTS_DIR):
        os.mkdir(REPORTS_DIR)
    
    today = date.today().strftime("%Y-%m-%d")
    filepath = os.path.join(REPORTS_DIR, f"brief_{today}.txt")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("AI Career Sentinel - Daily Brief\n")
        f.write(f"Date: {today}\n")
        f.write("=" * 50 + "\n\n")
        f.write(brief)

    print(f"[Filesystem MCP] Report saved to: {filepath}")
    return filepath

def list_past_reports() -> list:
    if not os.path.exists(REPORTS_DIR):
        return []
    files = sorted(os.listdir(REPORTS_DIR), reverse=True)
    return [os.path.join(REPORTS_DIR, f) for f in files if f.endswith(".txt")]