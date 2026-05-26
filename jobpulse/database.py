import sqlite3
import hashlib
from jobpulse.config import DB_PATH
from datetime import datetime, timezone

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracked_jobs (
        job_id TEXT PRIMARY KEY,
        company TEXT NOT NULL,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        date_discovered TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def generate_job_id(company, title, url):
    key = f"{company}{title}{url}".lower().strip()
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

def is_job_tracked(job_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM tracked_jobs WHERE job_id = ?", (job_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def track_job(job_id, company, title, url):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    date_discovered = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
    INSERT INTO tracked_jobs (job_id, company, title, url, date_discovered)
    VALUES (?, ?, ?, ?, ?)
    """, (job_id, company, title, url, date_discovered))
    conn.commit()
    conn.close()

def filter_unseen_and_track(company, title, url):
    job_id = generate_job_id(company, title, url)
    if not is_job_tracked(job_id):
        track_job(job_id, company, title, url)
        return True
    return False

