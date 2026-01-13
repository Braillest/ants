import os
import requests
from celery import Celery

backend = os.getenv("CELERY_RESULT_BACKEND")
broker = os.getenv("CELERY_BROKER_URL")
worker = Celery("ants", backend=backend, broker=broker)
worker.config_from_object("config.worker")

@worker.task
def add(x, y):
    return x + y
