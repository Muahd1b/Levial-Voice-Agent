import os
import logging
import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("email_manager")

mcp = FastMCP("Email Manager")

def get_imap_connection():
    """Connect to IMAP server."""
    imap_server = os.environ.get("EMAIL_IMAP_SERVER", "imap.gmail.com")
    email_user = os.environ.get("EMAIL_USER")
    email_pass = os.environ.get("EMAIL_PASSWORD")
    
    if not email_user or not email_pass:
        raise ValueError("EMAIL_USER and EMAIL_PASSWORD env vars must be set.")
        
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_user, email_pass)
    return mail

def clean_text(html_content: str) -> str:
    """Strip HTML tags."""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()

@mcp.tool()
def fetch_unread_emails(limit: int = 5) -> str:
    """
    Fetch unread emails from the Inbox.
    """
    try:
        mail = get_imap_connection()
        mail.select("inbox")
        
        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        
        if not email_ids:
            return "No unread emails."
            
        # Get the latest 'limit' emails
        latest_email_ids = email_ids[-limit:]
        
        result = "Unread Emails:\n"
        for e_id in latest_email_ids:
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From")
                    
                    result += f"- From: {from_} | Subject: {subject}\n"
                    
                    # Extract body snippet?
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                result += f"  Snippet: {body[:100]}...\n"
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                        result += f"  Snippet: {body[:100]}...\n"
                        
        mail.logout()
        return result
    except Exception as e:
        return f"Error fetching emails: {str(e)}"

# Note: Drafting requires Gmail API (SMTP is for sending).
# For simplicity in this MVP, we'll skip the drafting tool implementation here 
# as it duplicates the Google Auth logic from Calendar. 
# We can add it later or merge with Calendar server if we want a "Google Suite" server.

if __name__ == "__main__":
    mcp.run()
