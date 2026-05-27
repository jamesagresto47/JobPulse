import json
import os
import hashlib
from jobpulse.config import DB_PATH  # Keeping this import; make sure DB_PATH ends in '.json' (e.g., /data/jobs.json)
from datetime import datetime, timezone

def _load_data():
    """Helper function to load the JSON database into memory."""
    # Convert DB_PATH to an absolute path so dirname is never empty
    abs_path = os.path.abspath(DB_PATH)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    
    if os.path.exists(abs_path):
        try:
            with open(abs_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def _save_data(data):
    """Helper function to write the entire in-memory database out to disk/GCS."""
    abs_path = os.path.abspath(DB_PATH)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w") as f:
        json.dump(data, f, indent=4)

def init_db():
    """Initializes the structural schema if the JSON file is missing or empty."""
    data = _load_data()
    # If the JSON doesn't contain our tracking map, initialize it
    if "tracked_jobs" not in data:
        data["tracked_jobs"] = {}
        _save_data(data)

def generate_job_id(company, title, url):
    key = f"{company}{title}{url}".lower().strip()
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

def is_job_tracked(job_id):
    data = _load_data()
    tracked_jobs = data.get("tracked_jobs", {})
    return job_id in tracked_jobs

def track_job(job_id, company, title, url):
    data = _load_data()
    if "tracked_jobs" not in data:
        data["tracked_jobs"] = {}
        
    date_discovered = datetime.now(timezone.utc).isoformat()
    
    # Store the job data using the job_id as the primary key mirror
    data["tracked_jobs"][job_id] = {
        "company": company,
        "title": title,
        "url": url,
        "date_discovered": date_discovered
    }
    _save_data(data)

def filter_unseen_and_track(company, title, url):
    job_id = generate_job_id(company, title, url)
    if not is_job_tracked(job_id):
        track_job(job_id, company, title, url)
        return True
    return False