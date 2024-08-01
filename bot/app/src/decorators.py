"""
Supporting functionality: decorators
"""

import logging
from functools import wraps
import asyncio
import io
from PIL import Image
from src.collection_of_info import is_user_allowed, is_enough_balance_for_image

def decorator_logging(func):
    """Decorator to log function calls and returns"""
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
        async def wrapper(*args, **kwargs):
            logger.info(f"Function {func.__name__} was called with {args} and {kwargs}")
            result = await func(*args, **kwargs)
            if isinstance(result, (Image.Image, io.BytesIO)):
                logger.info(f"Function {func.__name__} returned an image")
            else:
                logger.info(f"Function {func.__name__} returned {result}")
            return result
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


def decorator_check_if_user_is_allowed(func):
    """Async wrapper which check if user is allowed
    If yes - proceed with function, if return string - "User is not allowed" """
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = args[0].message.from_user.id
            if await is_user_allowed(user_id):
                return await func(*args, **kwargs)
            else:
                update = args[0]
                await update.message.reply_text("User is not allowed")
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = args[0].message.from_user.id
            if is_user_allowed(user_id):
                return func(*args, **kwargs)
            else:
                return "User is not allowed"
    return wrapper


def decorator_has_enough_money_for_picture(func):
    """Decorator which checks if user has enough money to get a picture"""
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = args[0].message.from_user.id
            if await is_enough_balance_for_image(user_id):
                return await func(*args, **kwargs)
            else:
                update = args[0]
                await update.message.reply_text("You don't have enough money to get a picture")
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = args[0].message.from_user.id
            if is_enough_balance_for_image(user_id):
                return func(*args, **kwargs)
            else:
                return "You don't have enough money to get a picture"
    return wrapper
