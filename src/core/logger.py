# src/core/logger.py
import logging, os
from logging.handlers import RotatingFileHandler

def setup_logger():
    if not os.path.exists('logs'): os.makedirs('logs')
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_file = 'logs/execution.log'
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2, encoding='utf-8')
    handler.setFormatter(log_formatter)
    logger = logging.getLogger('OpenAgentLogger')
    logger.setLevel(logging.INFO)
    if not logger.handlers: logger.addHandler(handler)
    return logger

logger = setup_logger()