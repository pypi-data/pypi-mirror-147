import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(levelname)s - %(name)s %(asctime)s - %(message)s"
)
logger = logging.getLogger("paymob-next")


def log(msg, level, **kwargs):
    getattr(logger, level)(msg, **kwargs)
