import os

from dotenv import load_dotenv
load_dotenv()

TARGET_CSV_PATH = os.environ.get("TARGET_CSV_PATH", "companies.csv")
DB_PATH = os.environ.get("DB_PATH", "job_tracker_state.db")

INCLUSION_KEYWORDS = ['python', 'software', 'developer', 'engineer', 'analyst', 'data', 'rust', 'backend', 'machine learning', 'ml']
EXCLUSION_KEYWORDS = ['senior', 'lead', 'principal', 'manager', 'director', 'intern', 'co-op', 'sr.', 'vp']

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
TIMEOUT = 10
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_USER_ID = os.environ.get("DISCORD_USER_ID")
