import logging
import os
from .config import BASE_DIR

LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, 'sosmpc.log')

logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger("sosmpc")

def get_logger(name: str) -> logging.Logger:
    """Retorna uma instância de logger filha."""
    return logging.getLogger(name)
