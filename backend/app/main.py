from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .router import handle_query
from .config import settings

app = FastAPI(
    title="AI INGRES Chatbot",
    description="MVP API for Smart India Hackathon 2025 groundwater chatbot",
    version="0.1.0"
)
 
class ChatRequest(BaseModel):
    query: str
    lang: str = "en"

@app.get("/")
def root():
    return {"message": "AI INGRES Chatbot API running"}

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Main chat endpoint. Accepts a query and language,
    routes it to the appropriate agent, and returns the result.
    """
    response = handle_query(request.query, request.lang)
    return response
