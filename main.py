import logging
from scraper import job_ad_scrapper
from utils import read_urls_from_excel, get_random_urls
from logger_setup import setup_logging
import os

# Setup logging
setup_logging()

# Define the path to the Excel file relative to the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_file_path = os.path.join(current_directory, 'portals_for_testing.xlsx')

# Read URLs from Excel
url_list = read_urls_from_excel(excel_file_path)

# Get random URLs
company_url_list = get_random_urls(url_list)

# Start scraping
all_unique_words = set()
for url in company_url_list:
    logging.info(f"Starting scrape for {url}")
    all_unique_words.update(job_ad_scrapper(url))

# Print all unique words found
print("Unique words found:")
for word in all_unique_words:
    print(word)
