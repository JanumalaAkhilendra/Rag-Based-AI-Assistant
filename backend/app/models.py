import os
import requests
from dotenv import load_dotenv

load_dotenv()   

def get_llm_answer(query, context):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise Exception("GROQ_API_KEY environment variable not set")
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",  # or "llama3-70b-8192", "mixtral-8x7b-32768", etc.
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
    )
    data = response.json()
    if response.status_code != 200 or "choices" not in data:
        raise Exception(f"Groq API error: {data}")
    return data["choices"][0]["message"]["content"]