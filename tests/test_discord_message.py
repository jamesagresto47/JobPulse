import sys
import os

# 1. Dynamically add the jobpulse directory to sys.path so the imports resolve
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'jobpulse'))
sys.path.insert(0, PARENT_DIR)

# 2. Import your actual logic and configuration
try:
    from jobpulse.notifier import send_discord_dm
    from jobpulse.config import DISCORD_BOT_TOKEN, DISCORD_USER_ID
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Looked in: {PARENT_DIR}")
    sys.exit(1)

def run_live_discord_test():
    print("--- Starting Live Discord Notification Test ---")
    
    # 3. Create a dummy CSV file to satisfy the file attachment requirement
    dummy_csv_filename = "dummy_report.csv"
    print(f"Creating temporary file: {dummy_csv_filename}...")
    with open(dummy_csv_filename, "w") as f:
        f.write("company,title,url\n")
        f.write("Mock AI Corp,Junior Python AI Developer,https://example.com/mock-job-1\n")

    # 4. Define example objects (fake job listings)
    test_jobs = [
        {
            'company': 'Mock AI Corp', 
            'title': 'Junior Python AI Developer', 
            'url': 'https://example.com/mock-job-1'
        },
        {
            'company': 'Test Stack Labs', 
            'title': 'Backend Infrastructure Engineer', 
            'url': 'https://example.com/mock-job-2'
        }
    ]
    
    # 5. Execute the actual function with your real credentials
    print(f"Attempting to send DM to User ID: {DISCORD_USER_ID}...")
    try:
        send_discord_dm(test_jobs, dummy_csv_filename)
        print("\n Success! Check your Discord DMs. If you didn't receive it, verify your bot tokens.")
    except Exception as e:
        print(f"\n❌ Failed to send message. Error encountered:\n{e}")
    finally:
        # 6. Clean up the dummy file we created
        if os.path.exists(dummy_csv_filename):
            os.remove(dummy_csv_filename)
            print(f"Cleaned up temporary file: {dummy_csv_filename}")

if __name__ == "__main__":
    run_live_discord_test()