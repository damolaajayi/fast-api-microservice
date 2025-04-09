import datetime
from time import sleep
from app.core.celery_config import celery_app


@celery_app.task
def send_email_task(email: str):
    print(f"Sending email to {email}...")
    sleep(5)  # Simulate a long-running task
    print(f"Email sent to {email}!")
    
@celery_app.task
def generate_weekly_report():
    print(f"Generating weekly report...{datetime.now()}")
