from celery import Celery
import difflib
import logging
import os
import requests
import redis

backend = os.getenv("CELERY_RESULT_BACKEND")
broker = os.getenv("CELERY_BROKER_URL")
drone = Celery("ants", backend=backend, broker=broker)
drone.config_from_object("config.drone")
redis_client = redis.from_url(backend or "redis://ants_development_queen_redis:6379/0")

queen_url = os.getenv("QUEEN_URL")
character_x_count = 32
character_y_count = 26
space_character = "\u2800"
remove_trailing_whitespace = True
TRANSLATION_TABLE = ["braille-patterns.cti", "en-ueb-g2.ctb"]
PUNCT_MAP = {
    "“": '"',
    "”": '"',
    "‘": "'",
    "’": "'",
    "—": "--",
    "–": "-",
    "…": "...",
}

# Health check.
@drone.task
def health():
    return True

# Query queen for stored document and store it in redis under the specified key.
@drone.task
def file_storage_to_redis(sub_url, redis_key):
    url = f"{queen_url}/{sub_url}"
    queen_response = requests.get(url)

    # Handle if request fails.
    if queen_response.status_code != 200:
        logging.error(f"Failed to download document {url}")
        return None

    queen_data = queen_response.json()

    # Handle if error is present.
    if "error" in queen_data:
        logging.error(f"Failed to get contents from {url}")
        logging.error(queen_data["error"])
        return None

    # Handle if contents is not present.
    if "contents" not in queen_data:
        logging.error(f"Failed to get contents from {url}")
        return None

    queen_contents = queen_data["contents"]
    redis_client.set(redis_key, queen_contents)
    return None

# Query redis and upload it to queen file storage under the specified key.
@drone.task
def upload_document(redis_key, sub_url):
    url = f"{queen_url}/{sub_url}"
    redis_response = redis_client.get(redis_key)

    # Handle if redis client does not return a value.
    if redis_response is None:
        logging.error(f"Failed to get redis data {redis_key}")
        return None

    redis_data = redis_response.decode("utf-8")
    queen_response = requests.post(url, json=redis_data)

    # Handle if request fails.
    if queen_response.status_code != 200:
        logging.error(f"Failed to upload document {url}")
        return None

    queen_data = queen_response.json()

    # Handle if error is present.
    if "error" in queen_data:
        logging.error(f"Failed to upload document {url}")
        logging.error(queen_data["error"])
        return None

    return None

# TODO: task to upload queen repo to github

# TODO: task to upload molds to thingiverse

# TODO: task to import molds from thingiverse into printables
