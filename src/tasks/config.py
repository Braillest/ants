import os

# --------------------
# Global defaults
# --------------------

enable_utc = True
timezone = "America/Chicago"

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

task_track_started = False
worker_hijack_root_logger = False

task_routes = {
    "worker.*": {"queue": "worker"},
    "drone.*": {"queue": "drone"},
}

# --------------------
# Worker defaults
# --------------------

worker = dict(
    enable_utc=enable_utc,
    timezone=timezone,
    task_serializer=task_serializer,
    result_serializer=result_serializer,
    accept_content=accept_content,
    task_track_started=task_track_started,
    worker_hijack_root_logger=worker_hijack_root_logger,
    task_routes=task_routes,
    task_default_queue="worker",
    worker_pool="prefork",
    worker_concurrency=os.cpu_count(),
    worker_prefetch_multiplier=1,
    # worker_max_tasks_per_child=10,
    # worker_max_memory_per_child=12288,  # 20 * 1024 = 20 MB,
    # task_acks_late=True,
    # task_reject_on_worker_lost=True,
    # task_soft_time_limit=25 * 60,
    # task_time_limit=30 * 60,
)

# --------------------
# Drone defaults
# --------------------

drone = dict(
    enable_utc=enable_utc,
    timezone=timezone,
    task_serializer=task_serializer,
    result_serializer=result_serializer,
    accept_content=accept_content,
    task_track_started=task_track_started,
    worker_hijack_root_logger=worker_hijack_root_logger,
    task_routes=task_routes,
    task_default_queue="drone",
    worker_pool="gevent",
    worker_concurrency=200,
    worker_prefetch_multiplier=10,
    # task_acks_late=False,
    # task_soft_time_limit=4 * 60,
    # task_time_limit=5 * 60,
)
