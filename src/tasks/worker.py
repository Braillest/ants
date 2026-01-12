import os
import requests
from celery import Celery

backend = os.getenv("CELERY_RESULT_BACKEND")
broker = os.getenv("CELERY_BROKER_URL")
celery = Celery("worker", backend=backend, broker=broker)

@celery.task
def add(x, y):
    return x + y
