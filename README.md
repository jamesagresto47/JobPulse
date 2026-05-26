# JobPulse: Automated Daily Job Scraper & Tracker

JobPulse is a local command-line tool that parses a CSV list of target companies, extracts active job postings from their career pages, filters them by custom skill criteria, identifies newly added positions, and generates a daily delta report.

## Features
- **CSV Ingestion:** Reads a local target list of companies.
- **Scraping Engine:** Modular web scraping with a generic fallback and potential for specific ATS integration.
- **Skill Filtering:** Matches job titles against predefined inclusion and exclusion keywords.
- **State Management:** Tracks previously seen jobs in a local SQLite database (`job_tracker_state.db`) to ensure deduplication.
- **Reporting:** Outputs a terminal summary and a CSV report for new job findings, with extensibility for Webhook notifications.

## Setup
1. **Requirements:** Python 3.10+
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configuration:**
   Update `jobpulse/config.py` with your custom inclusion/exclusion keywords, or set environment variables like `TARGET_CSV_PATH` and `WEBHOOK_URL`.
4. **Target File:**
   Provide a CSV file named `Job Application Tracker - Copy of Target Companies.csv` in the root folder with columns ordered as: Company, City, State, Career URL, Contact, Industry.

## Usage
Run the script to discover new jobs:
```bash
python jobpulse/main.py
```