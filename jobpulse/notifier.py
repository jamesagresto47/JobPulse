import csv
import json
from datetime import datetime
import requests
import logging

from jobpulse.config import DISCORD_BOT_TOKEN, DISCORD_USER_ID

def print_terminal_report(new_jobs):
    if not new_jobs:
        print("0 new matching jobs identified today.")
        return

    print(f"{len(new_jobs)} new matching jobs identified today.\n")
    print(f"{'Company':<20} | {'Title':<40} | {'URL'}")
    print("-" * 100)
    for job in new_jobs:
        company = job['company'][:18]
        title = job['title'][:38]
        url = job['url']
        print(f"{company:<20} | {title:<40} | {url}")

def save_csv_report(new_jobs):
    if not new_jobs:
        return None
        
    date_str = datetime.now().strftime("%Y-%m-%d, %H:%M")
    filename = f"job_reports/report_{date_str}.csv"
    
    # Sort by State, then City, then Company for location grouping
    sorted_jobs = sorted(new_jobs, key=lambda x: (x.get('state', ''), x.get('city', ''), x.get('company', '')))
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Company', 'Title', 'URL', 'Industry', 'City', 'State'])
        for job in sorted_jobs:
            writer.writerow([
                job['company'], 
                job['title'], 
                job['url'], 
                job.get('industry', ''),
                job.get('city', ''),
                job.get('state', '')
            ])
            
    return filename
            

def send_discord_dm(new_jobs, csv_filename):
    if not DISCORD_BOT_TOKEN or not DISCORD_USER_ID:
        return

    new_jobs_count = len(new_jobs)
    try:
        # 1. Create a DM channel with the user
        headers = {
            "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        create_dm_url = "https://discord.com/api/v10/users/@me/channels"
        dm_payload = {"recipient_id": DISCORD_USER_ID}
        
        dm_response = requests.post(create_dm_url, headers=headers, json=dm_payload, timeout=10)
        dm_response.raise_for_status()
        channel_id = dm_response.json().get("id")
        
        if not channel_id:
            logging.warning("Failed to get DM channel ID from Discord.")
            return

        # 2. Build out all message lines
        all_lines = [
            f"🚀 **JobPulse Report**", 
            f"Identified **{new_jobs_count}** new matching jobs today!\n"
        ]
        
        for job in new_jobs:
            all_lines.append(f"• **{job['company']}**: [{job['title']}](<{job['url']}>)")

        # 3. Chunk lines into separate messages staying under the 2,000 character limit
        messages_to_send = []
        current_chunk = []
        current_length = 0

        for line in all_lines:
            # Check if adding this line (plus a newline character) exceeds our safety threshold
            if current_length + len(line) + 1 > 1900:
                messages_to_send.append("\n".join(current_chunk))
                current_chunk = [line]
                current_length = len(line)
            else:
                current_chunk.append(line)
                current_length += len(line) + 1

        # Append the final remaining chunk if it exists
        if current_chunk:
            messages_to_send.append("\n".join(current_chunk))

        # 4. Transmit the messages over the Discord API
        send_message_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        msg_headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
        
        # Open CSV file to attach it safely to the very first message packet
        with open(csv_filename, 'rb') as f:
            files = {'file': (csv_filename, f, 'text/csv')}
            
            for i, chunk_content in enumerate(messages_to_send):
                message_payload = {"content": chunk_content}
                
                if i == 0:
                    # First message gets the multi-part form data containing the file upload
                    data = {'payload_json': json.dumps(message_payload)}
                    msg_response = requests.post(send_message_url, headers=msg_headers, data=data, files=files, timeout=15)
                else:
                    # Successive overflow chunks go out as clean, standard JSON payloads
                    import time
                    time.sleep(0.5)  # Quick buffer gap to keep Discord's rate limiter happy
                    msg_response = requests.post(send_message_url, headers={"Authorization": f"Bot {DISCORD_BOT_TOKEN}", "Content-Type": "application/json"}, json=message_payload, timeout=15)
                
                msg_response.raise_for_status()
            
    except requests.RequestException as e:
        logging.warning(f"Failed to send Discord DM: {e}")
def notify_all(new_jobs):
    print_terminal_report(new_jobs)
    csv_filename = save_csv_report(new_jobs)
    if new_jobs:
        if csv_filename:
            send_discord_dm(new_jobs, csv_filename)
