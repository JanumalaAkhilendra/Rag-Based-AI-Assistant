from sentence_transformers import SentenceTransformer
import chromadb

# Use a persistent directory for ChromaDB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("personal_assistant")

model = SentenceTransformer("BAAI/bge-base-en-v1.5")

def embed_text(text):
    return model.encode([text])[0]

def get_vector_store():
    return collection