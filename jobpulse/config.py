import os

from dotenv import load_dotenv
load_dotenv()

# 1. Get the directory path from the environment, defaulting to the current directory locally
DB_DIR = os.getenv("DB_DIR", ".")

# 2. CRITICAL: Ensure DB_PATH points to the FILE inside that directory, not just the directory itself
DB_PATH = os.path.join(DB_DIR, "job_tracker_state.json")

TARGET_CSV_PATH = os.environ.get("TARGET_CSV_PATH", "companies.csv")
DB_PATH = os.environ.get("DB_PATH", "job_tracker_state.json")

INCLUSION_KEYWORDS = ['python', 'software', 'developer', 'engineer', 'analyst', 'data', 'rust', 'backend', 'machine learning', 'ml']
EXCLUSION_KEYWORDS = ['senior', 'lead', 'principal', 'manager', 'director', 'intern', 'co-op', 'sr.', 'vp']

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
TIMEOUT = 10
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_USER_ID = os.environ.get("DISCORD_USER_ID")
