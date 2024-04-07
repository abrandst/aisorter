import imaplib
import email
from email.header import decode_header
import os



class Mail:
    def login(self):
        # Login to IMAP server        
        imap_url = os.environ.get("IMAP_URL")
        user = os.environ.get("IMAP_USER")
        password = os.environ.get("IMAP_PASSWORD")

        self.mail = imaplib.IMAP4_SSL(imap_url)
        self.mail.login(user, password)
        print("Login to IMAP server")
        return self.mail

    def getFolderContent(self,folder):
        # Select the mailbox you want to use. INBOX is default
        self.mail.select(folder)

        # Search for all emails in the inbox
        status, messages = self.mail.search(None, 'ALL')
        messages = messages[0].split()
        return messages
    

    def move(self,email_id,label):        
        # The command could vary based on the server. For Gmail, it's usually 'COPY' then 'STORE' with '\\Deleted' flag
        result = self.mail.copy(email_id, label)
        if result[0] == 'OK':
            self.mail.store(email_id, '+FLAGS', '\\Deleted')  # Mark the email for deletion in the original folder
            self.mail.expunge()  # Purge emails marked for deletion
            print(f"Email {email_id} moved to {label} successfully.")
        else:
            print("Failed to move the email.")

    def copy(self,email_id,label):
        # Move the selected email to 'NewFolder'
        # The command could vary based on the server. For Gmail, it's usually 'COPY' then 'STORE' with '\\Deleted' flag
        result = self.mail.copy(email_id, label)
        if result[0] == 'OK':
            print(f"Email {email_id} moved to {label} successfully.")
        else:
            print("Failed to move the email.")

    def get_text(self,mail_id):
        status, data = self.mail.fetch(mail_id, 'BODY[]')
        #status, data = self.mail.fetch(mail_id, '(RFC822)')
        if status != 'OK':
            print(f"Error fetching email {mail_id}.")
            raise Exception("failed to fetch email")

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
        return email_body

        
        
