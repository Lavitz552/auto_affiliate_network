import threading
import time
from .affiliate import schedule_content_generation

def continuous_scheduler(interval=1800):
    """
    Runs the content generation and scaling logic continuously every `interval` seconds (default: 30 minutes).
    """
    def job():
        while True:
            print("[Scheduler] Running automated content and scaling tasks...")
            schedule_content_generation()
            time.sleep(interval)
    t = threading.Thread(target=job, daemon=True)
    t.start()
