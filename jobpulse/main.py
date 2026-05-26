import pandas as pd
import os
import sys
import logging

from jobpulse.config import TARGET_CSV_PATH
from jobpulse.database import init_db, filter_unseen_and_track
from jobpulse.scraper import get_jobs
from jobpulse.filter import is_relevant_job
from jobpulse.notifier import notify_all

logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s', filename='jobpulse_errors.log')

def process_target_csv():
    if not os.path.exists(TARGET_CSV_PATH):
        logging.warning(f"Target CSV file not found: {TARGET_CSV_PATH}")
        return []
        
    try:
        # No header row, accessed by zero-indexed positions
        df = pd.read_csv(TARGET_CSV_PATH, header=None)
    except Exception as e:
        logging.warning(f"Failed to read CSV: {e}")
        return []

    targets = []
    for index, row in df.iterrows():
        try:
            url = str(row[3]).strip()
            # Robust checks
            if pd.isna(row[3]) or not url.startswith(('http://', 'https://')):
                continue
                
            targets.append({
                'company': str(row[0]).strip(),
                'city': str(row[1]).strip() if not pd.isna(row[1]) else '',
                'state': str(row[2]).strip() if not pd.isna(row[2]) else '',
                'url': url,
                'contact': str(row[4]).strip() if not pd.isna(row[4]) else None,
                'industry': str(row[5]).strip() if not pd.isna(row[5]) else ''
            })
        except Exception as e:
            logging.warning(f"Skipping row {index} due to error: {e}")
            
    return targets

def main():
    init_db()
    targets = process_target_csv()
    total_targets = len(targets)
    
    new_matching_jobs = []
    
    print(f"Starting job scrape for {total_targets} companies...\n")
    for i, target in enumerate(targets, 1):
        # Clean progress display
        sys.stdout.write(f"\r\033[K[{i}/{total_targets}] Scraping {target['company'][:30]}...")
        sys.stdout.flush()
        
        company_jobs = get_jobs(target['url'], target['company'])
        
        for job in company_jobs:
            if is_relevant_job(job['title']):
                if filter_unseen_and_track(job['company'], job['title'], job['url']):
                    job['industry'] = target['industry']
                    job['city'] = target['city']
                    job['state'] = target['state']
                    new_matching_jobs.append(job)
                    
    sys.stdout.write("\r\033[KScraping complete.\n\n")
    sys.stdout.flush()
    notify_all(new_matching_jobs)

if __name__ == "__main__":
    main()
