import logging
from logging.handlers import TimedRotatingFileHandler

from settings import settings


def setup_logging() -> None:
    handlers = [
        logging.StreamHandler(),
        TimedRotatingFileHandler(filename=settings.log_file, when="midnight"),
    ]
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        handlers=handlers
    )
    logging.getLogger("watchfiles").setLevel(logging.WARNING)
