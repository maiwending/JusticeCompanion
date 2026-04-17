from gmail_watcher import GmailWatcher

def print_message_info(message):
    headers = message['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
    print(f"New email from: {sender}")
    print(f"Subject: {subject}")
    # Extract plain text body
    parts = message['payload'].get('parts', [])
    for part in parts:
        if part['mimeType'] == 'text/plain':
            import base64
            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            print(f"Body:\n{body}")

if __name__ == "__main__":
    watcher = GmailWatcher()
    watcher.watch_for_email("system@smartinmate.com", print_message_info, poll_interval=10)