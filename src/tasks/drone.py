import os
import requests
from celery import Celery

backend = os.getenv("CELERY_RESULT_BACKEND")
broker = os.getenv("CELERY_BROKER_URL")
drone = Celery("ants", backend=backend, broker=broker)
drone.config_from_object("config.drone")

@drone.task
def add(x, y):
    return x + y
