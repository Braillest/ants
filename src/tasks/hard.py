import os
import re
import difflib
import logging
import unicodedata
import tempfile
from celery import Celery
import redis
import louis
from build123d import *
import io

from config import mold as mold_config

backend = os.getenv("CELERY_RESULT_BACKEND")
broker = os.getenv("CELERY_BROKER_URL")
worker = Celery("ants", backend=backend, broker=broker)
worker.config_from_object("config.worker")
redis_client = redis.from_url(backend or "redis://ants_development_queen_redis:6379/0")

queen_url = os.getenv("QUEEN_URL")

# Config-derived globals
character_x_count = mold_config["cell_x_count"]
character_y_count = mold_config["cell_y_count"]
space_character = mold_config["space_character"]

# Task globals
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
@worker.task
def health():
    return True

# Task to query redis and generate mold
@worker.task
def generate_positive_mold(redis_key_a, redis_key_b):
    redis_response = redis_client.get(redis_key_a)

    # Handle if redis client does not return a value.
    if redis_response is None:
        logging.error(f"Failed to get redis data {redis_key_a}")
        return None

    braille_text = redis_response.decode("utf-8")
    lines = braille_text.splitlines()

    # Load configuration
    scaling_factor = mold_config["scaling_factor"]
    space_character = mold_config["space_character"]
    paper_d = mold_config["paper_d"]
    cell_y_count = mold_config["cell_y_count"]
    slot_w = mold_config["slot_w"]
    paper_tolerance = mold_config["paper_tolerance"]
    cell_w = mold_config["cell_w"]
    cell_padding_x = mold_config["cell_padding_x"]
    cell_h = mold_config["cell_h"]
    cell_padding_y = mold_config["cell_padding_y"]
    cell_spacing = mold_config["cell_spacing"]
    pin_w = mold_config["pin_w"]
    pin_h = mold_config["pin_h"]
    pin_d = mold_config["pin_d"]
    positive_mold_backplate_d = mold_config["positive_mold_backplate_d"]
    dot_d = mold_config["dot_d"]
    dot_r = mold_config["dot_r"]
    positive_mold_w = mold_config["positive_mold_w"]
    positive_mold_h = mold_config["positive_mold_h"]

    # Generate dot coordinates
    dot_coords = []
    for line_index, line in enumerate(lines[0:cell_y_count]):
        x_offset = slot_w + paper_tolerance + (3 * cell_w) + cell_padding_x
        y_offset = (cell_y_count - line_index) * cell_h + cell_padding_y
        text = line.rstrip()

        for character in text:
            delta = ord(character) - ord(space_character)
            binary = f"{delta:06b}"[::-1]
            for i, (dx, dy) in enumerate([(0, 2), (0, 1), (0, 0), (1, 2), (1, 1), (1, 0)]):
                if binary[i] == "1":
                    dot_coords.append((
                        x_offset + dx * cell_spacing,
                        y_offset + dy * cell_spacing,
                        positive_mold_backplate_d + (dot_d / 2)
                    ))
            x_offset += cell_w

    # Generate positive mold
    with BuildPart() as positive_mold:
        # Create backplate aligned to the positive quadrant (Align.MIN)
        backplate = Box(
            positive_mold_w, 
            positive_mold_h, 
            positive_mold_backplate_d, 
            align=(Align.MIN, Align.MIN, Align.MIN)
        )

        # Create and add the left and right side rails.
        rail_template = Box(slot_w, positive_mold_h, positive_mold_backplate_d + paper_d)
        left_rail_location = (slot_w / 2, positive_mold_h / 2, positive_mold_backplate_d + paper_d / 2)
        right_rail_location = (positive_mold_w - slot_w / 2, positive_mold_h / 2, positive_mold_backplate_d + paper_d / 2)
        add(Compound(children=Locations([left_rail_location, right_rail_location]) * rail_template))

        # Create a list of all left side pin locations.
        left_pin_locations = []
        for y_index in range(0, cell_y_count, 2):
            left_pin_locations.append((slot_w / 2, y_index * cell_h, positive_mold_backplate_d + paper_d + (pin_d / 2)))

        # Create a list of all right side pin locations.
        right_pin_locations = []
        for y_index in range(0, cell_y_count, 2):
            right_pin_locations.append((positive_mold_w - slot_w / 2, y_index * cell_h, positive_mold_backplate_d + paper_d + (pin_d / 2)))

        # Create the left side pins.
        pin_template = Box(pin_w, pin_h, pin_d)
        # Draft the right edge to have a 30 degree overhang.
        left_pin_template = pin_template.draft(
            axis=(0, 1, 0),
            angle=30,
        )
        add(Compound(children=Locations(left_pin_locations) * left_pin_template))

        # Create and add the left and right side pins.
        right_pin_template = pin_template.draft(
            axis=(0, -1, 0),
            angle=30,
        )
        add(Compound(children=Locations(right_pin_locations) * right_pin_template))

        # Add dots.
        if dot_coords:
            dot_template = Sphere(dot_r, arc_size1=0)
            add(Compound(children=Locations(dot_coords) * dot_template))

        # Scale the mold in the X and Y dimensions to account for shrinkage.
        positive_mold_object = positive_mold.part.scale(scaling_factor, scaling_factor, 1)

        # Export the scaled mold to a BytesIO buffer and set it in redis.
        with io.BytesIO() as buffer:
            export_stl(positive_mold_object, buffer, tolerance=0.1, angular_tolerance=1)
            redis_client.set(redis_key_b, buffer.getvalue())

    return None

# Strip project gutenberg header and footer.
@worker.task
def strip_gutenberg_header_footer(redis_key_a, redis_key_b):
    START = r"\*\*\* START OF (THIS|THE) PROJECT GUTENBERG EBOOK .* \*\*\*"
    END   = r"\*\*\* END OF (THIS|THE) PROJECT GUTENBERG EBOOK .* \*\*\*"

    redis_response = redis_client.get(redis_key_a)

    # Handle if redis clinet does not return a value
    if redis_response is None:
        logging.error(f"Failed to get redis data {document_id_a}")
        return None

    text = redis_response.decode("utf-8")
    text = re.split(START, text, maxsplit=1)[-1]

    # Handle if regex does not return a value.
    if text is None:
        logging.error(f"Failed to strip gutenberg header and footer from {redis_key_a}")
        return None

    text = re.split(END, text, maxsplit=1)[0]

    # Handle if regex does not return a value.
    if text is None:
        logging.error(f"Failed to strip gutenberg header and footer from {redis_key_a}")
        return None

    redis_client.set(redis_key_b, text)
    return None

# Query redis and serialize document/remove offending characters.
@worker.task
def serialize_document(redis_key_a, redis_key_b):
    redis_response = redis_client.get(redis_key_a)

    # Handle if redis clinet does not return a value.
    if redis_response is None:
        logging.error(f"Failed to get redis data {redis_key_a}")
        return None

    # Strip offending characters.
    text = redis_response.decode("utf-8")

    # Remove control and non-printing characters.
    text = "".join(
        ch for ch in text
        if not unicodedata.category(ch).startswith("C")
    )

    # Normalize punctuation.
    for k, v in PUNCT_MAP.items():
        text = text.replace(k, v)

    # Remove hyphenation at line breaks.
    text = re.sub(r"-\n(\w)", r"\1", text)

    # Remove illustations, footnotes, and artifacts.
    text = re.sub(r"\[Illustration.*?\]", "", text, flags=re.I)
    text = re.sub(r"\[Footnote.*?\]", "", text, flags=re.I)
    text = re.sub(r"\[Art.*?\]", "", text, flags=re.I)

    # Remove emphasis lines and divider lines.
    text = re.sub(r"_+", "", text)
    text = re.sub(r"\*+", "", text)

    # Restrict to braille-safe characters.
    ALLOWED = set("abcdefghijklmnopqrstuvwxyz"
                  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                  "0123456789"
                  " .,;:'\"!?()-\n")
    text = "".join(ch for ch in text if ch in ALLOWED)

    # Save to redis.
    redis_client.set(redis_key_b, text)
    return None


# Query redis and generate a git diff between original and modified formats.
# NOTE: Used in multiple steps.
@worker.task
def diff_documents(redis_key_a, redis_key_b, redis_key_c):

    text_a = redis_client.get(redis_key_a)

    # Handle if redis client does not return a value.
    if text_a is None:
        logging.error(f"Failed to get redis data {redis_key_a}")
        return None

    lines_a = text_a.decode("utf-8").split("\n")

    # Handle if lines_a is empty.
    if not lines_a:
        logging.error(f"Failed to split redis data {redis_key_a}")
        return None

    text_b = redis_client.get(redis_key_b)

    # Handle if redis client does not return a value.
    if text_b is None:
        logging.error(f"Failed to get redis data {redis_key_b}")
        return None

    lines_b = text_b.decode("utf-8").split("\n")

    # Handle if lines_b is empty.
    if not lines_b:
        logging.error(f"Failed to split redis data {redis_key_b}")
        return None

    diff = difflib.unified_diff(lines_a, lines_b)
    diff_text = "\n".join(diff)

    # Handle if diff_text is empty.
    if not diff_text:
        logging.warning(f"No difference between {redis_key_a} and {redis_key_b}")
        return None

    redis_client.set(redis_key_c, diff_text)
    return None

# Query redis and use liblouis to translate document to braille.
@worker.task
def translate_document(redis_key_a, redis_key_b):
    text = redis_client.get(redis_key_a)

    # Handle if redis client does not return a value.
    if text is None:
        logging.error(f"Failed to get redis data {redis_key_a}")
        return None

    text = text.decode("utf-8")
    lines = text.split("\n")
    braille_lines = []

    for line in lines:
        if remove_trailing_whitespace:
            line = line.rstrip()
        braille_lines.append(louis.translateString(TRANSLATION_TABLE, line))
    braille_text = "\n".join(braille_lines)

    # Handle if braille_text is empty.
    if not braille_text:
        logging.error(f"Failed to translate {redis_key_a}")
        return None

    redis_client.set(redis_key_b, braille_text)
    return None

# Query redis and use liblouis to backtranslate document to text.
@worker.task
def backtranslate_document(redis_key_a, redis_key_b):
    text = redis_client.get(redis_key_a)

    # Handle if redis client does not return a value.
    if text is None:
        logging.error(f"Failed to get redis data {redis_key_a}")
        return None

    text = text.decode("utf-8")
    lines = text.split("\n")
    text_lines = []

    for line in lines:
        if remove_trailing_whitespace:
            line = line.rstrip()
        text_lines.append(louis.backtranslateString(TRANSLATION_TABLE, line))
    text_text = "\n".join(text_lines)

    # Handle if text_text is empty.
    if not text_text:
        logging.error(f"Failed to backtranslate {redis_key_a}")
        return None

    redis_client.set(redis_key_b, text_text)
    return None

# Query redis and format braille to specified format (eg braillest standard).
@worker.task
def format_braille(redis_key_a, redis_key_b):
    text = redis_client.get(redis_key_a)

    # Handle if redis client does not return a value.
    if text is None:
        logging.error(f"Failed to get redis data {redis_key_a}")
        return None

    pattern = r"([^\n]+(?:\n[^\n]+)*)"
    text = text.decode("utf-8")
    matches = re.finditer(pattern, text)
    offset = 0

    for match in matches:

        # Convert list of text to string
        match_text = match.group(0).replace("\n", space_character)
        match_words = match_text.split(space_character)
        current_line = ""
        wrapped_lines = []

        # Iterate through each word
        for word in match_words:

            word_len = len(word)

            # Incoming word can fit case
            if len(current_line) + word_len + 1 <= character_x_count:

                # If it's not the first word, prepend a space
                if current_line:
                    current_line += space_character

                current_line += word

            # Incoming word cannot fit case
            else:

                # Special conditional for braille line break
                if word_len < character_x_count:
                    wrapped_lines.append(current_line)

                current_line = word

        # Add the last line if exists
        if current_line:
            wrapped_lines.append(current_line)

        wrapped_text = "\n".join(wrapped_lines)
        start = match.start() + offset
        end = match.end() + offset
        text = text[:start] + wrapped_text + text[end:]
        delta = len(wrapped_text) - len(match_text)
        offset += delta

    redis_client.set(redis_key_b, text)
    return None

# Query redis and paginate braille.
@worker.task
def paginate_braille(redis_key_a, redis_key_b):
    pages = []
    current_page = []
    current_page_size = 0

    text = redis_client.get(redis_key_a)

    # Handle if redis client does not return a value.
    if text is None:
        logging.error(f"Failed to get redis data {redis_key_a}")
        return None

    text = text.decode("utf-8")

    # TODO:
    # Alter pagination to prevent dividing table of contents lines from their page number / page breaking within a line

    formatted_braille_lines = text.split("\n")
    for line_index, line in enumerate(formatted_braille_lines):

        if line.strip() != '' or current_page:
            current_page_size += 1
            current_page.append(line)

        if len(current_page) >= character_y_count:

            # Chunk text
            pattern = r"([^\n]+(?:\n[^\n]+)*)"
            text = "".join(current_page)
            matches = list(re.finditer(pattern, text))
            last_match_text = matches[-1].group(0).replace("\n", space_character)
            line_break_string = "⠿" * character_x_count

            # Handle case that line break occurs at end of page.
            if line_break_string in last_match_text:

                # Remove line_break_string from current page,
                # Add current page to output
                # Start new page with line_break_string
                current_page = current_page[:current_page_size - 1]
                pages.append(current_page)
                current_page = [line]
                current_page_size = 1
                continue

            # Add page, reset current page
            pages.append(current_page)
            current_page = []
            current_page_size = 0

    if current_page:
        pages.append(current_page)

    redis_client.set(redis_key_b, pages)
    return None

# Generate cover-art from stored html.
@worker.task
def generate_cover_art(redis_key_a, query_string, selector, redis_key_b):
    redis_response = redis_client.get(redis_key_a)

    # Handle if redis client does not return a value.
    if redis_response is None:
        logging.error(f"Failed to get redis data {redis_key_a}")
        return None

    html = redis_response.decode("utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html)
        page.goto(f'about:blank?{query_string}')
        element = page.wait_for_selector(selector)
        screenshot = element.screenshot()
        browser.close()

    redis_client.set(redis_key_b, screenshot)

    return None
