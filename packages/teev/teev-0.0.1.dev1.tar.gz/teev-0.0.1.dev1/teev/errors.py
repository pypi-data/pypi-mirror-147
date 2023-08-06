import traceback
from teev.log import logger


def log_error(add_text=""):
    err = traceback.format_exc()
    if add_text:
        err += f"\n{add_text}"
    logger.error(err)


def error_handler(func):
    async def wrapped(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception:
            log_error()

    return wrapped
