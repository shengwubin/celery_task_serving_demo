import os
import random

from celery import Celery
from dotenv import load_dotenv

load_dotenv(override=False)

app = Celery('tasks')

app.conf.broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')


def is_retry_task():
    return random.random() < 0.2


@app.task(bind=True, max_retries=10)
def add(self, x, y):
    if is_retry_task():
        raise self.retry(countdown=2)

    return x + y
