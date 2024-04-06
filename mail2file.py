import imaplib
import email
import os
from email.header import decode_header

def save_email_to_file(email_body, email_id):
    filename = f'mail/email_{email_id}.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(email_body)

# Login to IMAP server
imap_url = 'imap.gmail.com'
user = os.environ.get("IMAP_USER")
password = os.environ.get("IMAP_PASSWORD")

# Connect to the Gmail IMAP server
mail = imaplib.IMAP4_SSL(imap_url)
mail.login(user, password)

# Select the mailbox you want to use. INBOX is default
mail.select('inbox')

# Search for all emails in the inbox
status, messages = mail.search(None, 'ALL')
if status != 'OK':
    print("No messages found!")
    exit()

# Convert the list of messages to a list of email IDs
messages = messages[0].split()

# Fetch the first 100 email IDs
num_emails = min(100, len(messages))
for i in range(num_emails):
    print(i)
    status, data = mail.fetch(messages[i], '(RFC822)')
    if status != 'OK':
        print(f"Error fetching email {i+1}.")
        continue

    # Parse the raw email content
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Initialize email body
    email_body = ""
    
    # Assuming the email is multipart
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # look for text/plain parts, but skip attachments
            if content_type == "text/plain" and "attachment" not in content_disposition:
                # get the email body
                try:
                    email_body = part.get_payload(decode=True).decode()
                except(UnicodeDecodeError):
                    continue
                break
    # Non-multipart emails (plain text, no attachments)
    else:
        email_body = msg.get_payload(decode=True).decode()

    if email_body:
        save_email_to_file(email_body, i+1)
    else:
        print(f"No text/plain content found for email {i+1}.")

mail.close()
mail.logout()
