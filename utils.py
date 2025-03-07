import os
import logging
from flask.logging import create_logger
from flask import Flask


app = Flask(__name__)

logger_app = create_logger(app)
logger_app.setLevel(logging.ERROR)


def handle_exception(e):
    logger_app.error("Error", exc_info=True)
    return str(e)

log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

file_handler = logging.FileHandler(os.path.join(log_directory, "app.log"))
file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
logger_app.addHandler(file_handler)



def is_valid(value):
    if isinstance(value, (int, float)) and str(value).isdigit():
        return True
    return False


def format_ask(value):
    if isinstance(value, str):
        parts = value.split(',')
        cleaned_parts = ["".join(filter(lambda x: x.isdigit(), part)) for part in parts]
        cleaned_parts = [part for part in cleaned_parts if part]

        if len(cleaned_parts) == 1:
            return int(cleaned_parts[0])

        elif len(cleaned_parts) == 2:
            return f"{int(cleaned_parts[0])},{int(cleaned_parts[1])}"

    return value if isinstance(value, int) else None




