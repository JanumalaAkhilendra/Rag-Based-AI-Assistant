class BaseIngestor:
    def ingest(self):
        raise NotImplementedError
    def update(self):
        raise NotImplementedError