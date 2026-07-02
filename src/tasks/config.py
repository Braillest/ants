import os
import math

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
    "hard.*": {"queue": "hard"},
    "soft.*": {"queue": "soft"},
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
    task_default_queue="hard",
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
    task_default_queue="soft",
    worker_concurrency=200,
    worker_prefetch_multiplier=10,
    # task_acks_late=False,
    # task_soft_time_limit=4 * 60,
    # task_time_limit=5 * 60,
)

# --------------------
# Mold definitions
# --------------------

scaling_factor = 1.005
space_character = "\u2800"

paper_w = 216
paper_h = 280
paper_d = 0.2
paper_tolerance = 0.25

cell_w = 6
cell_h = 10
cell_padding_x = 1.75
cell_padding_y = 2.5
cell_spacing = 2.5

pin_w = 4.5
pin_h = 9.8
pin_d = 1.2

slot_w = 5
slot_h = 10
slot_d = pin_d

dot_r = 0.75
dot_d = 0.5 + paper_d

hole_r = 0.95
hole_d = dot_d + paper_d

negative_mold_w = slot_w + paper_tolerance + paper_w + paper_tolerance + slot_w
negative_mold_h = paper_h
negative_mold_d = pin_d

positive_mold_w = slot_w + paper_tolerance + paper_w + paper_tolerance + slot_w
positive_mold_h = paper_h
positive_mold_backplate_d = 1.0
positive_mold_rail_d = positive_mold_backplate_d + paper_d
positive_mold_d = positive_mold_rail_d + negative_mold_d

left_cell_padding_count = 3
right_cell_padding_count = 1
top_cell_padding_count = 1
bottom_cell_padding_count = 1

max_cell_x_count = math.floor(paper_w / cell_w)
cell_x_count = max_cell_x_count - left_cell_padding_count - right_cell_padding_count

max_cell_y_count = math.floor(paper_h / cell_h)
cell_y_count = max_cell_y_count - top_cell_padding_count - bottom_cell_padding_count

mold = dict(
    scaling_factor = scaling_factor,
    space_character = space_character,

    paper_w = paper_w,
    paper_h = paper_h,
    paper_d = paper_d,
    paper_tolerance = paper_tolerance,

    cell_w = cell_w,
    cell_h = cell_h,
    cell_padding_x = cell_padding_x,
    cell_padding_y = cell_padding_y,
    cell_spacing = cell_spacing,

    pin_w = pin_w,
    pin_h = pin_h,
    pin_d = pin_d,

    slot_w = slot_w,
    slot_h = slot_h,
    slot_d = slot_d,

    dot_r = dot_r,
    dot_d = dot_d,

    hole_r = hole_r,
    hole_d = hole_d,

    negative_mold_w = negative_mold_w,
    negative_mold_h = negative_mold_h,
    negative_mold_d = negative_mold_d,

    positive_mold_w = positive_mold_w,
    positive_mold_h = positive_mold_h,
    positive_mold_backplate_d = positive_mold_backplate_d,
    positive_mold_rail_d = positive_mold_rail_d,
    positive_mold_d = positive_mold_d,

    left_cell_padding_count = left_cell_padding_count,
    right_cell_padding_count = right_cell_padding_count,
    top_cell_padding_count = top_cell_padding_count,
    bottom_cell_padding_count = bottom_cell_padding_count,

    max_cell_x_count = max_cell_x_count,
    cell_x_count = cell_x_count,

    max_cell_y_count = max_cell_y_count,
    cell_y_count = cell_y_count,
)
