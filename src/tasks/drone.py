import os
import requests
from celery import Celery

backend = os.getenv("CELERY_RESULT_BACKEND")
broker = os.getenv("CELERY_BROKER_URL")
drone = Celery("ants", backend=backend, broker=broker)
drone.config_from_object("config.drone")

queen_url = os.getenv("QUEEN_URL")

@drone.task
def add(x, y):
    return x + y

# TODO: task to query queen for stored document, download it, and store it in redis

# TODO: task to query redis and upload it to queen file storage

# TODO: task to query redis and serialize document/remove offending characters

# TODO: task to query redis and generate a git diff between original and modified formats
# NOTE: Used in multiple steps

# TODO: task to query redis and use liblouis to translate document to braille

# TODO: task to query redis and use liblouis to backtranslate document to text
# NOTE: Used in multiple steps

# TODO: task to query redis and format braille to specified format (eg braillest standard)

# TODO: task to query redis and paginate braille

# TODO: task to generate cover-art

# TODO: task to upload queen repo to github

# TODO: task to upload molds to thingiverse

# TODO: task to import molds from thingiverse into printables
