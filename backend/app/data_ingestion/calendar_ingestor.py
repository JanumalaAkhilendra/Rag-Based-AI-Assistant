import os
import pickle
import uuid
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from .base import BaseIngestor
from app.vector_store import embed_text, get_vector_store
from app.db import get_db_connection

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token_calendar.pickle')

class CalendarIngestor(BaseIngestor):
    def get_service(self):
        creds = None
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        service = build('calendar', 'v3', credentials=creds)
        return service

    def fetch_events(self, max_results=10):
        service = self.get_service()
        events_result = service.events().list(
            calendarId='primary', maxResults=max_results, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def ingest(self):
        events = self.fetch_events()
        vector_store = get_vector_store()
        conn = get_db_connection()
        for event in events:
            summary = event.get('summary', 'No Title')
            start = event['start'].get('dateTime', event['start'].get('date'))
            description = event.get('description', '')
            text = f"Event: {summary}\nTime: {start}\nDescription: {description}"
            embedding = embed_text(text)
            meta = {"summary": summary, "start": start}
            vector_store.add(
                ids=[str(uuid.uuid4())],
                documents=[text],
                embeddings=[embedding],
                metadatas=[{
                    "source": "calendar",
                    "summary": summary,
                    "start": start,
                    "role": "me"
                }]
            )
            with conn:
                conn.execute(
                    "INSERT INTO data_chunks (source, text, meta, role) VALUES (?, ?, ?, ?)",
                    ("calendar", text, str(meta), "me")
                )
        conn.close()