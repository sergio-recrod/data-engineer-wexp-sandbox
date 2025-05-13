import logging
import sys

def setup_logger(
    logger_name: str,
    level: int = logging.INFO,
    file_name: str = None,
) -> logging.Logger:
    """Build a logger instance.

    Parameters
    ----------
    logger_name : str
        name of logger.
    level : int, optional
        logger level (e.g., logging.DEBUG, logging.WARNING etc.), by default
        logging.INFO.
    file_name : str, optional
        logger filename, if needed to write logs to file, by default None
        meaning log messages will not be written to file.

    Returns
    -------
    logging.Logger
        a logger instance with the requested properties.

    """
    # set up the logger and logging level
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # fix the logger format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # set up a stream handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(sh)

    # set up logger file handler
    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger