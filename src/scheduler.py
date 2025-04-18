import threading
import time
from .affiliate import schedule_content_generation

def continuous_scheduler(interval=1800):
    """
    Runs the content generation and scaling logic continuously every `interval` seconds (default: 30 minutes).
    """
    def job():
        print("[Scheduler] Running initial content and scaling tasks...")
        schedule_content_generation()  # Run once immediately
        while True:
            print("[Scheduler] Waiting for next scheduled run...")
            time.sleep(interval)
            print("[Scheduler] Running scheduled content and scaling tasks...")
            schedule_content_generation()
    t = threading.Thread(target=job, daemon=True)
    t.start()
