import logging
from functools import wraps
import asyncio
import io
from PIL import Image

def decorator_logging(func):
    logging.basicConfig(
        #format='timestamp=%(asctime)s logger=%(name)s level=%(levelname)s msg="%(message)s"',
        format='{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "msg": "%(message)s"}',
        datefmt='%Y-%m-%dT%H:%M:%S',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("./logs/bot.log"),
            logging.StreamHandler()
        ]
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger.info(f"Function {func.__name__} was called with {args} and {kwargs}")
            result = await func(*args, **kwargs)
            if isinstance(result, (Image.Image, io.BytesIO)):
                logger.info(f"Function {func.__name__} returned an image")
            else:
                logger.info(f"Function {func.__name__} returned {result}")
            return result
        return async_wrapper
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Function {func.__name__} was called with {args} and {kwargs}")
            result = func(*args, **kwargs)
            if isinstance(result, (Image.Image, io.BytesIO)):
                logger.info(f"Function {func.__name__} returned an image")
            else:
                logger.info(f"Function {func.__name__} returned {result}")
            return result
        return wrapper