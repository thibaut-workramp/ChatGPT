import logging
from functools import reduce


def set_logging_level(log_level: str):
    logging.basicConfig()
    if log_level.lower() == 'error':
        logging.getLogger().setLevel(logging.ERROR)
    elif log_level.lower() == 'info':
        logging.getLogger().setLevel(logging.INFO)
    elif log_level.lower() == 'debug':
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        raise ValueError(f'Unknown log_level: {log_level}')


def concat_two_str(str1, str2):
    return f'{str1}{str2}'


def concat_strs(list_of_str: list) -> str:
    concatenated_strs = reduce(concat_two_str, list_of_str) if len(list_of_str) != 0 else ''
    return concatenated_strs
