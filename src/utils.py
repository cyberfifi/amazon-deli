import logging
import yaml


def get_logger():
    format_ = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=format_)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


def get_credentials():
    with open('./credentials.yaml', 'r') as stream:
        data = yaml.safe_load(stream)
        return data
