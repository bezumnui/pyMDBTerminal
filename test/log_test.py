import datetime
import logging


def test():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(datetime.datetime.now().strftime("mdb_log_%d.%m.%Y_%H.%M.%S"))
    stream_handler = logging.StreamHandler()

    file_handler.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')

if __name__ == '__main__':
    test()
