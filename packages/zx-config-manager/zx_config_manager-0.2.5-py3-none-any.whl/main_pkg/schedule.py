from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler(schedule_func, interval_seconds=60):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=schedule_func, trigger="interval", seconds=interval_seconds)
    scheduler.start()