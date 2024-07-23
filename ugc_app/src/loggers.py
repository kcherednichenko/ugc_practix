import logging
from logging.handlers import TimedRotatingFileHandler

from asgi_correlation_id import CorrelationIdFilter

from settings import settings


def setup_logging() -> None:
    handlers = [
        logging.StreamHandler(),
        TimedRotatingFileHandler(filename=settings.log_file, when="midnight"),
    ]
    cid_filter = CorrelationIdFilter()
    for handler in handlers:
        handler.addFilter(cid_filter)
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [req_id:%(correlation_id)s] %(message)s"
            )
        )
    logging.basicConfig(level=logging.INFO, handlers=handlers)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)
