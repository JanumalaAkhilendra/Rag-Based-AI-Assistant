from .base import BaseIngestor
from app.vector_store import embed_text, get_vector_store
from app.db import get_db_connection
import uuid
import re
import os

class WhatsAppIngestor(BaseIngestor):
    def ingest(self, file_path=None):
        # Default file path if not provided
        if file_path is None:
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "whatsapp_chat.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"WhatsApp chat file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        vector_store = get_vector_store()
        conn = get_db_connection()
        for line in lines:
            # Example line: "12/31/21, 10:00 PM - Alice: Happy New Year!"
            match = re.match(r"^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s*[ap]m) - ([^:]+): (.+)$", line)
            if match:
                date, time, sender, message = match.groups()
                text = f"{sender} on {date} at {time}: {message}"
                embedding = embed_text(text)
                meta = {"sender": sender, "date": date, "time": time}
                vector_store.add(
                    ids=[str(uuid.uuid4())],
                    documents=[text],
                    embeddings=[embedding],
                    metadatas=[{
                        "source": "whatsapp",
                        "sender": sender,
                        "date": date,
                        "time": time,
                        "role": "me"
                    }]
                )
                with conn:
                    conn.execute(
                        "INSERT INTO data_chunks (source, text, meta, role) VALUES (?, ?, ?, ?)",
                        ("whatsapp", text, str(meta), "me")
                    )
        conn.close()
