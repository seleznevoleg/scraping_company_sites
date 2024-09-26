import requests
from bs4 import BeautifulSoup
import logging
import os
import time
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

# Set up logging, clearing the log file at the start
log_filename = 'scraper.log'
if os.path.exists(log_filename):
    os.remove(log_filename)

logging.basicConfig(filename=log_filename, level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s')

company_url_list = ['http://www.kiessling-spedition.de/', 'https://air-sys.de/','https://www.trixitt.de/jobs','http://www.evmberlin.de','http://www.schweiger-gmbh.com']
# company_url_list = ['https://www.phv-dialyse.de/']


job_ad_menu_phrases = ['job', 'jobs', 'career', 'karriere', 'stelle', 'unternehmen', 'stellenangebote']
job_ad_phrases = ['m/w/d', 'er*in', 'w/m/d', 'r/in', 'm/f/d', 'all genders']

visited_urls = set()

def find_job_pages(url):
    # logging.debug(f"Scraping job menu links from {url}")
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        links = soup.find_all("a")  # Find all elements with the tag <a>
        filtered_links = []
        for link in links:
            link_text = link.get_text(strip=True).replace('\u00AD', '').lower()
            href = link.get("href")
            if link_text and href and any(phrase in link_text for phrase in job_ad_menu_phrases):
                filtered_links.append(href)
                logging.debug(f"Found link: {href} with text: {link_text}")
            elif href:
                print(href)
                # logging.debug(f"No job menu links were found on {href}")

        return filtered_links
    except requests.exceptions.RequestException as e:
        # logging.error(f"Error fetching {url}: {e}")
        return []

def job_ad_scrapper(url):
    if url in visited_urls:
        logging.debug(f"Already visited {url}, skipping.")
        return set()
    
    visited_urls.add(url)
    logging.debug(f"Scraping job ads from {url}")
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        final_url = response.url  # Get the final URL after redirection
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        # logging.info(soup)
        

        # Exclude script and style tags
        for script in soup(["script", "style"]):
            script.decompose()

        # Check if any element's text includes one of the job_ad_phrases
        found_elements = []
        for element in soup.find_all(string=True):
            element_text = element.strip()
            if any(phrase in element_text for phrase in job_ad_phrases):
                found_elements.append(element_text)
        
        if found_elements:
            logging.info(f"Job ads found in {final_url}:")
            for text in found_elements:
                logging.info(f" - {text}")
            return set(found_elements)
        else:
            logging.info(f"No job ads found in {final_url}, scraping for links.")
            links = find_job_pages(final_url)
            unique_words = set()
            for link in links:
                # Ensure the link is absolute
                if not link.startswith('http'):
                    link = requests.compat.urljoin(final_url, link)
                unique_words.update(job_ad_scrapper(link))
            return unique_words
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return set()

# Main loop
all_unique_words = set()
for url in company_url_list:
    logging.info(f"Starting scrape for {url}")
    all_unique_words.update(job_ad_scrapper(url))

# Print all unique words found
print("Unique words found:")
for word in all_unique_words:
    print(word)