import sqlite3
import os
import sys

# Add jobpulse to path to easily import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'jobpulse')))
from jobpulse.config import DB_PATH

def remove_one_job_per_company():
    # Because tests are run from a different directory, make sure DB_PATH is absolute or relative to root
    db_path = os.path.join(os.path.dirname(__file__), '..', DB_PATH)
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' does not exist yet. Run the main script first.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Select one job per company by grouping by company
        # Using MIN(job_id) ensures we consistently pick one specific row per company
        cursor.execute("""
            SELECT MIN(job_id), company, title 
            FROM tracked_jobs 
            GROUP BY company
        """)
        jobs_to_delete = cursor.fetchall()
        
        if not jobs_to_delete:
            print("The database is currently empty. No jobs to remove.")
            return
            
        deleted_count = 0
        print("Removing one job from each company...\n")
        
        for job_id, company, title in jobs_to_delete:
            cursor.execute("DELETE FROM tracked_jobs WHERE job_id = ?", (job_id,))
            deleted_count += 1
            print(f"[-] {company:<20} | Removed: {title[:50]}")
            
        conn.commit()
        print(f"\nSuccessfully removed {deleted_count} jobs (one from each company present in the database).")
            
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}. Has the table been created yet?")
        
    finally:
        conn.close()

if __name__ == "__main__":
    remove_one_job_per_company()
