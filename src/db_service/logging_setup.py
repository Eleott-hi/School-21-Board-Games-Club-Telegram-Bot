import logging

def setup_logger(name, log_file, level=logging.DEBUG):
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

if __name__ == "__main__":
    logger = setup_logger('logger_1', 'database_logging.py')
    logger.error(f"this is the test error")