import pandas as pd
import random
import logging

def read_urls_from_excel(file_path):
    """ Reads URLs from an Excel file and returns them as a list. """
    try:
        df = pd.read_excel(file_path)
        if 'Website' not in df.columns:
            logging.error("The Excel file does not contain a 'Website' column.")
            return []
        
        urls = df['Website'].dropna().tolist()
        logging.info(f"Loaded {len(urls)} URLs from Excel file.")
        return urls
    except FileNotFoundError as e:
        logging.error(f"File not found: {file_path}")
        return []
    except Exception as e:
        logging.error(f"Error reading the Excel file: {e}")
        return []

def get_random_urls(url_list, count=5):
    """ Selects random URLs from the provided list. """
    if len(url_list) < count:
        logging.warning("URL list has fewer entries than the requested random count.")
        return url_list
    return random.sample(url_list, count)
