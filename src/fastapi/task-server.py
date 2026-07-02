from fastapi import FastAPI
from celery import Celery
import os
import redis

celery_broker = os.getenv("CELERY_BROKER_URL")
celery_backend = os.getenv("CELERY_RESULT_BACKEND")
celery = Celery("task-server", broker=celery_broker, backend=celery_backend)
redis_client = redis.from_url(celery_backend or "redis://host.docker.internal:6379/0")

# Manual config
celery.conf.update(
    enable_utc = True,
    timezone = "America/Chicago",
    task_serializer = "json",
    result_serializer = "json",
    accept_content = ["json"],
    task_track_started = False,
    worker_hijack_root_logger = False,
    task_routes = {
        "hard.*": {"queue": "hard"},
        "soft.*": {"queue": "soft"},
    }
)

app = FastAPI(title="Ants Task Bridge", version="0.0.1", root_path="/job")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test")
def test():
    hard_test = celery.send_task("hard.health")
    soft_test = celery.send_task("soft.health")
    return {"status": "ok"}

@app.post("/submit")
def submit_task(payload: dict):
    print(payload)
    return {"status": "ok"}
