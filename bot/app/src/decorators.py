from datetime import datetime
# clas decorator logging which inits logging and then logs function calls
import logging
from functools import wraps
# https://stackoverflow.com/questions/69786048/how-to-use-class-attributes-in-method-decorators-in-python
def decorator_logging(func):
    logging.basicConfig(
        format='timestamp=%(asctime)s logger=%(name)s level=%(levelname)s msg="%(message)s"',
        datefmt='%Y-%m-%dT%H:%M:%S',
        level=logging.INFO,
        handlers=[
            logging.StreamHandler()
        ]
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Function {func.__name__} was called by {args[0].message.from_user.id}")
        return func(*args, **kwargs)
    
    return wrapper

# class decorator_logging which inits logging and then logs function calls
import logging
from functools import wraps

class decorator_logging:
    def __init__(self, func):
        logging.basicConfig(
            format='timestamp=%(asctime)s logger=%(name)s level=%(levelname)s msg="%(message)s"',
            datefmt='%Y-%m-%dT%H:%M:%S',
            level=logging.INFO,
            handlers=[
                logging.StreamHandler()
            ]
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)
        self.func = func

    def __call__(self, *args, **kwargs):
        self.logger.info(f"Function {self.func.__name__} was called by {args[0].message.from_user.id}")
        return self.func(*args, **kwargs)
    


# loger that we save messages
logger.inof(user_message)