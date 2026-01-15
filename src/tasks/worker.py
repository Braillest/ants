import os
from celery import Celery

backend = os.getenv("CELERY_RESULT_BACKEND")
broker = os.getenv("CELERY_BROKER_URL")
worker = Celery("ants", backend=backend, broker=broker)
worker.config_from_object("config.worker")

queen_url = os.getenv("QUEEN_URL")

@worker.task
def add(x, y):
    return x + y

# TODO: task to query redis and generate mold
