import sqlite3
import os
import sys

# Add jobpulse to path to easily import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'jobpulse')))
from jobpulse.config import DB_PATH

def clear_all_jobs():
    db_path = os.path.join(os.path.dirname(__file__), '..', DB_PATH)
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' does not exist yet. Run the main script first.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Delete all rows from tracked_jobs table
        cursor.execute("DELETE FROM tracked_jobs")
        deleted_count = cursor.rowcount
        conn.commit()
        print(f"Successfully removed all {deleted_count} jobs from the database.")
        print("The database is now completely empty.")
            
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}. Has the table been created yet?")
        
    finally:
        conn.close()

if __name__ == "__main__":
    clear_all_jobs()
