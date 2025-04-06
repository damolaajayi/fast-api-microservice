from celery import Celery



calery_app = Celery('worker', 
                    broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/0',)

celery_app.conf.task_routes = {
    'app.workers.tasks.senf_email_task': {'queue': 'email'},
}