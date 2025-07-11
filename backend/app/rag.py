from app.vector_store import get_vector_store, embed_text
from app.models import get_llm_answer


def answer_query(query, role, source=None):
    query_emb = embed_text(query)
    vector_store = get_vector_store()
    where = {"role": role}
    if source:
        where = {"$and": [{"role": role}, {"source": source}]}
    results = vector_store.query(
        query_embeddings=[query_emb],
        n_results=5,
        where=where
    )
    docs = results['documents'][0]
    metadatas = results['metadatas'][0]
    context = "\n".join(docs)
    print("Context passed to LLM:", context)
    answer = get_llm_answer(query, context)
    references = metadatas
    return answer, references