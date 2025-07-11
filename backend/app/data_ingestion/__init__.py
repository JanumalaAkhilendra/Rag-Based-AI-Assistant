from .gmail_ingestor import GmailIngestor
from .calendar_ingestor import CalendarIngestor
from .whatsapp_ingestor import WhatsAppIngestor

SOURCES = {
    "gmail": GmailIngestor(),
    "calendar": CalendarIngestor(),
    "whatsapp": WhatsAppIngestor(),
}

def ingest_source(source):
    SOURCES[source].ingest()