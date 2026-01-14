from celery import Celery
import difflib
import liblouis
import logging
import os
import requests

backend = os.getenv("CELERY_RESULT_BACKEND")
broker = os.getenv("CELERY_BROKER_URL")
drone = Celery("ants", backend=backend, broker=broker)
drone.config_from_object("config.drone")

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

@drone.task
def add(x, y):
    return x + y

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

# Strip project gutenberg header and footer.
@drone.task
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
@drone.task
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
@drone.task
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
@drone.task
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
@drone.task
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
@drone.task
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
@drone.task
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
@drone.task
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

# TODO: task to upload queen repo to github

# TODO: task to upload molds to thingiverse

# TODO: task to import molds from thingiverse into printables
