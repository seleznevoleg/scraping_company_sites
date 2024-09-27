import logging
import os
import time

def setup_logging():
    """ Sets up logging with a dynamic log file name based on the current date and time. """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_filename = f"{log_dir}/scraper_{time.strftime('%Y-%m-%d_%H-%M-%S')}.log"
    logging.basicConfig(filename=log_filename, level=logging.DEBUG, 
                        format='%(asctime)s %(levelname)s: %(message)s')
    logging.info("Logging setup complete.")
