# # # import sys
# # # import os
# # # sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # # from agents.scraper import scrape_fresh_jobs
# # # from agents.rag_matcher import match_jobs_to_resume
# # # from agents.scorer import score_all_jobs
# # # from agents.brief_writer import write_morning_brief
# # # from telegram_bot.notifier import send_telegram_brief

# # # def run_career_sentinel():
# # #     print("\n🚀 AI Career Sentinel Starting...\n")

# # #     # Step 1 — Scrape fresh jobs
# # #     fresh_jobs = scrape_fresh_jobs()
# # #     if not fresh_jobs:
# # #         print("[Main] No fresh jobs found today. Try again later.")
# # #         return

# # #     # Step 2 — RAG match against resume
# # #     top_jobs = match_jobs_to_resume(fresh_jobs)

# # #     # Step 3 — Claude scores each job
# # #     scored_jobs = score_all_jobs(top_jobs)

# # #     # Step 4 — Claude writes morning brief
# # #     brief = write_morning_brief(scored_jobs)
# # #     print("\n📋 YOUR MORNING BRIEF:\n")
# # #     print(brief)

# # #     # Step 5 — Send to Telegram
# # #     send_telegram_brief(brief)

# # #     print("\n✅ AI Career Sentinel Done!\n")

# # # if __name__ == "__main__":
# # #     run_career_sentinel()


# # import sys
# # import os
# # sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # from agents.scraper import scrape_fresh_jobs
# # from agents.rag_matcher import match_jobs_to_resume
# # from agents.scorer import score_all_jobs
# # from agents.brief_writer import write_morning_brief
# # from telegram_bot.notifier import send_telegram_brief
# # from mcp_tools.filesystem_mcp import save_daily_report, list_past_reports

# # def run_career_sentinel():
# #     print("\n🚀 AI Career Sentinel Starting...\n")
# #     print("[MCP] Fetch MCP + Filesystem MCP active\n")

# #     # Step 1 — Scraper Agent + Fetch MCP (full JDs)
# #     fresh_jobs = scrape_fresh_jobs()
# #     if not fresh_jobs:
# #         print("[Main] No fresh jobs found today. Try again later.")
# #         return

# #     # Step 2 — RAG match against resume
# #     top_jobs = match_jobs_to_resume(fresh_jobs)

# #     # Step 3 — Groq/Llama scores each job
# #     scored_jobs = score_all_jobs(top_jobs)

# #     # Step 4 — Write morning brief
# #     brief = write_morning_brief(scored_jobs)
# #     print("\n📋 YOUR MORNING BRIEF:\n")
# #     print(brief)

# #     # Step 5 — Filesystem MCP — save report locally
# #     report_path = save_daily_report(brief)

# #     # Step 6 — Send to Telegram
# #     send_telegram_brief(brief)

# #     # Show past reports count
# #     past = list_past_reports()
# #     print(f"\n[Filesystem MCP] Total reports saved: {len(past)}")
# #     print(f"[Filesystem MCP] Latest: {report_path}")
# #     print("\n✅ AI Career Sentinel Done!\n")

# # if __name__ == "__main__":
# #     run_career_sentinel()


# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from agents.scraper import scrape_fresh_jobs
# from agents.rag_matcher import match_jobs_to_resume
# from agents.scorer import score_all_jobs
# from agents.brief_writer import write_morning_brief
# from telegram_bot.notifier import send_telegram_brief

# def run_career_sentinel():
#     print("\n🚀 AI Career Sentinel Starting...\n")
#     print("[MCP] Fetch MCP active\n")

#     # Step 1 — Scraper Agent + Fetch MCP (full JDs)
#     fresh_jobs = scrape_fresh_jobs()
#     if not fresh_jobs:
#         print("[Main] No fresh jobs found today. Try again later.")
#         return

#     # Step 2 — RAG match against resume
#     top_jobs = match_jobs_to_resume(fresh_jobs)

#     # Step 3 — Groq/Llama scores each job
#     scored_jobs = score_all_jobs(top_jobs)

#     # Step 4 — Write morning brief
#     brief = write_morning_brief(scored_jobs)
#     print("\n📋 YOUR MORNING BRIEF:\n")
#     print(brief)

#     # Step 5 — Send to Telegram
#     send_telegram_brief(brief)

#     print("\n✅ AI Career Sentinel Done!\n")

# if __name__ == "__main__":
#     run_career_sentinel()



import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.scraper import scrape_fresh_jobs
from agents.rag_matcher import match_jobs_to_resume
from agents.scorer import score_all_jobs
from agents.brief_writer import write_morning_brief
from telegram_bot.notifier import send_telegram_brief
from mcp_tools.mcp_client import save_report_mcp

def run_career_sentinel():
    print("\n🚀 AI Career Sentinel Starting...\n")
    print("[MCP] Real MCP Server active — tools: fetch_job_description, save_report\n")

    # Step 1 — Scraper Agent + MCP fetch_job_description tool
    fresh_jobs = scrape_fresh_jobs()
    if not fresh_jobs:
        print("[Main] No fresh jobs found today. Try again later.")
        return

    # Step 2 — RAG match against resume
    top_jobs = match_jobs_to_resume(fresh_jobs)

    # Step 3 — Groq/Llama scores each job
    scored_jobs = score_all_jobs(top_jobs)

    # Step 4 — Write morning brief
    brief = write_morning_brief(scored_jobs)
    print("\n📋 YOUR MORNING BRIEF:\n")
    print(brief)

    # Step 5 — MCP save_report tool — save brief locally
    print("[MCP Client] Calling save_report tool via MCP protocol...")
    result = save_report_mcp(brief)
    print(f"[MCP Server] {result}")

    # Step 6 — Send to Telegram
    send_telegram_brief(brief)

    print("\n✅ AI Career Sentinel Done!\n")

if __name__ == "__main__":
    run_career_sentinel()