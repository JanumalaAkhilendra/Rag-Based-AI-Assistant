from .base import BaseIngestor
from app.vector_store import embed_text, get_vector_store
from app.db import get_db_connection
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import uuid
from pydantic import BaseModel

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token_gmail.pickle')

class GmailIngestor(BaseIngestor):
    def get_service(self):
        creds = None
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        service = build('gmail', 'v1', credentials=creds)
        return service

    def fetch_emails(self, max_results=10):
        service = self.get_service()
        results = service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            # Get body (plain text)
            body = ''
            if 'parts' in msg_data['payload']:
                for part in msg_data['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = part['body'].get('data', '')
                        break
            else:
                body = msg_data['payload']['body'].get('data', '')
            import base64
            import quopri
            if body:
                try:
                    body = base64.urlsafe_b64decode(body).decode('utf-8')
                except Exception:
                    body = quopri.decodestring(body).decode('utf-8', errors='ignore')
            emails.append({
                'subject': subject,
                'body': body,
                'from': sender,
                'date': date
            })
        return emails

    def ingest(self):
        emails = self.fetch_emails()
        vector_store = get_vector_store()
        conn = get_db_connection()
        for email in emails:
            text = f"Subject: {email['subject']}\n{email['body']}"
            embedding = embed_text(text)
            meta = {"from": email["from"], "date": email["date"]}
            vector_store.add(
                ids=[str(uuid.uuid4())],
                documents=[text],
                embeddings=[embedding],
                metadatas=[{
                    "source": "gmail",
                    "from": email["from"],
                    "date": email["date"],
                    "role": "me"
                }]
            )
            with conn:
                conn.execute(
                    "INSERT INTO data_chunks (source, text, meta, role) VALUES (?, ?, ?, ?)",
                    ("gmail", text, str(meta), "me")
                )
        conn.close()