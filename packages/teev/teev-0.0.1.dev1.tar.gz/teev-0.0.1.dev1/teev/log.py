import logging
from functools import lru_cache


@lru_cache(maxsize=None)
def _create_logger():
    # DEFINE LOGGING
    stream_format = logging.Formatter(
        "%(asctime)s.%(msecs)03d; %(levelname)s; %(processName)s; %(name)s; %(funcName)s=%(lineno)d; %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger("tgbotapi")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(stream_format)

    logger.addHandler(ch)
    return logger


logger = _create_logger()
