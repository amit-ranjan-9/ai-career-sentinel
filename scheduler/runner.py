from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import run_career_sentinel
import pytz

scheduler = BlockingScheduler()
ist = pytz.timezone("Asia/Kolkata")

scheduler.add_job(
    run_career_sentinel,
    trigger=CronTrigger(hour=8, minute=0, timezone=ist),
    name="AI Career Sentinel - Daily 8AM IST"
)

if __name__ == "__main__":
    print("⏰ AI Career Sentinel Scheduler Started!")
    print("📅 Will run every day at 8:00 AM IST")
    print("Press Ctrl+C to stop\n")
    scheduler.start()