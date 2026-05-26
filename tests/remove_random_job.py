import sqlite3
import os
import sys

# Add jobpulse to path to easily import config if needed, or just define DB_PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'jobpulse')))
from jobpulse.config import DB_PATH

def remove_random_job():
    db_path = os.path.join(os.path.dirname(__file__), '..', DB_PATH)
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' does not exist yet. Run the main script first.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Select one random job from the database
        cursor.execute("SELECT job_id, company, title, url FROM tracked_jobs ORDER BY RANDOM() LIMIT 1")
        job = cursor.fetchone()
        
        if job:
            job_id, company, title, url = job
            # Delete the randomly selected job
            cursor.execute("DELETE FROM tracked_jobs WHERE job_id = ?", (job_id,))
            conn.commit()
            print("Successfully removed a random job from the database for testing:")
            print(f"  Company: {company}")
            print(f"  Title:   {title}")
            print(f"  URL:     {url}")
        else:
            print("The database is currently empty. No jobs to remove.")
            
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}. Has the table been created yet?")
        
    finally:
        conn.close()

if __name__ == "__main__":
    remove_random_job()
