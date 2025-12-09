import logging, os
LOGFILE = os.path.join(os.getcwd(), 'fim_daemon.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGFILE),
        logging.StreamHandler()
    ]
)
def get_logger():
    return logging.getLogger('fim_daemon')
