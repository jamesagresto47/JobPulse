import requests
from bs4 import BeautifulSoup
import logging
from jobpulse.config import HEADERS, TIMEOUT
import urllib.parse

def parse_generic(url, company):
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.warning(f"Failed to fetch {url} for company {company}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []
    
    # Generic strategy: parse <a> tags for job keywords
    for a_tag in soup.find_all('a'):
        title = a_tag.get_text(strip=True)
        href = a_tag.get('href')
        
        if title and href:
            full_url = urllib.parse.urljoin(url, href)
            jobs.append({"title": title, "url": full_url, "company": company})
            
    return jobs

def get_jobs(url, company):
    # Specialized endpoint hooks would be placed here (e.g. Workday, Lever).
    return parse_generic(url, company)
