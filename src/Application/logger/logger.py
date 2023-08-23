import functools
import inspect
import os
import re
import json
import logging
import logging.config
import sys
from pathlib import Path
from time import strftime, gmtime

logging.getLogger('chardet.charsetprober').setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

# logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)


class Logger(object):
    def __init__(self, *args):
        pass

    def init_logging(self,
                     default_path='logger/logger.json',
                     default_level=logging.INFO,
                     env_key='LOG_CFG'
                     ):
        """Setup logging configuration
        """
        path = default_path
        value = os.getenv(env_key, None)
        Path("../logs").mkdir(parents=True, exist_ok=True)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
                log_path = f'./logs/logs_{strftime("%d-%m-%y-%H-%M-%S", gmtime())}'
                Path(log_path).mkdir(parents=True, exist_ok=True)
                for handler in config['handlers']:
                    try:
                        config["handlers"][handler][
                            "filename"] = f'{log_path}/{config["handlers"][handler]["filename"]}'
                        print(config["handlers"][handler]["filename"])
                        if not os.path.exists(f'{config["handlers"][handler]["filename"]}'):
                            open(f'{config["handlers"][handler]["filename"]}')
                    except:
                        pass
                logging.config.dictConfig(config)
        else:
            raise LookupError('There is no logger.json config file!')

        return logging


_logger = Logger().init_logging()


def rm_link_to_obj_in_memory(t):
    resub_pattern = '( object at [A-Z0-9x]{10,20})'
    return re.sub(resub_pattern, '', str(t))


def log_row(*args, **kwargs):
    '''
    returns formatted string
    '''
    try:
        frame = inspect.currentframe().f_back
        name = frame.f_code.co_name
        if name == 'wrapper':
            frame = frame.f_back
            name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        line = frame.f_lineno
        if name == "<module>":  # this is module name
            name = "........"
        ar = list(args)

        ar = [rm_link_to_obj_in_memory(str(a)) for a in ar]
        ar = ', '.join(ar)
        filename = filename.split('\\')[-1].split('/')[-1]
        return (f"[{filename}:{line}]\t[{name}]\targs: {ar}")
    finally:
        del frame


def loggerator(func):
    """
    this is logging decorator
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _logger.debug('[begin..] ' + log_row(*args, **kwargs))
        try:
            res = func(*args, **kwargs)
            _logger.info(
                f'[executed]\tfunction name: --{func.__name__}--\t{func.__doc__}\tresult:{res!r}')
        except Exception as EE:
            _logger.error(log_row(*args, **kwargs) + '\tException: ' + str(EE))
            pass
        else:
            _logger.debug('[finished] ' + log_row(*args, **kwargs) +
                          '\tres: ' + rm_link_to_obj_in_memory(str(res)))
            return res

    return wrapper


def setup_logger(name, log_file, level=logging.INFO, backupCount=10):
    """To setup as many loggers as you want"""
    formatter = logging.Formatter(
        '%(asctime)s | PID %(process)d.%(threadName)s | %(name)s | %(levelname)s | '
        'msg: %(message)s',
        '%Y-%m-%d %H:%M:%S'
    )
    handler = logging.handlers.RotatingFileHandler(
        "./logs/" + log_file, maxBytes=(100000000), backupCount=backupCount
    )
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
