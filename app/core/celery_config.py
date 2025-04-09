import os
from celery import Celery
from celery.schedules import crontab


broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

celery_app = Celery('worker', 
                    broker=broker_url,
                    backend=result_backend
)


celery_app.conf.update(
    task_routes={
        'app.workers.tasks.send_email_task': {'queue': 'email'},
        'app.workers.tasks.generate_weekly_report': {'queue': 'report'},
    },
    beat_schedule={
        'generate-weekly-report': {
            'task': 'app.workers.tasks.generate_weekly_report',
            'schedule': 60.0 * 60 * 24 * 7,  # Every week,
            #"schedule": crontab(hour=8, minute=0, day_of_week=1),  # Every Monday at 08:00 UTC

        },
    },
    timezone='UTC',

)