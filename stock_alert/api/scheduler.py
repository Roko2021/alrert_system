from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import fetch_and_check_alerts

scheduler = BackgroundScheduler()

def start():
    scheduler.add_job(fetch_and_check_alerts, 'interval', minutes=1)
    scheduler.start()
