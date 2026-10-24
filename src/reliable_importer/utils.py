from contextlib import contextmanager
import logging
from time import perf_counter

logger = logging.getLogger(__name__)


@contextmanager
def logged_operation(operation: str):
    logger.info("%s розпочато", operation)
    start = perf_counter()
    try:
        yield
    except Exception:
        logger.exception("%s завершилося з помилкою", operation)
        raise
    else:
        elapsed = perf_counter() - start
        logger.info("%s завершено за %.6f с", operation, elapsed)