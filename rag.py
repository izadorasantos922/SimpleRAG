# RAG

import os
import requests
from data import data_doc
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable not set")


app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_rag(request: QueryRequest):
    context = "\n".join([entry["text"] for entry in data_doc])

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"Answer based solely on the following documents:\n\n{context}\n\nQuestion: {request.query}\nAI answer:"}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data, params={"key": API_KEY})

    if response.status_code == 200:
        answer = response.json()
        return {"answer": answer['candidates'][0]['content']['parts'][0]['text']}
    else:
        return {"error": f"Failed to generate content. Status code: {response.status_code}", "details": response.text}
