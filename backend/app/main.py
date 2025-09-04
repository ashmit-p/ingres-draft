from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from .router import handle_query, init_agents, shutdown_agents
from .config import settings
import csv
import os

# Cache for CSV data
data_cache = []


def load_csv_data():
    """
    Load CSV data into memory.
    Called during startup or when a manual reload is needed.
    """
    global data_cache
    csv_path = os.path.join(os.path.dirname(__file__), "data", "reports.csv")

    if not os.path.exists(csv_path):
        raise FileNotFoundError("reports.csv not found")

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data_cache = list(reader)

    print(f"[INFO] Loaded {len(data_cache)} records from reports.csv")


def clear_csv_data():
    """Clear CSV cache from memory."""
    global data_cache
    data_cache.clear()
    print("[INFO] Data cache cleared")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan event handler.
    Runs once at startup and cleanup at shutdown.
    """
    # Startup
    load_csv_data()
    init_agents()

    yield  # API runs here

    # Shutdown
    clear_csv_data()
    shutdown_agents()


app = FastAPI(
    title="AI INGRES Chatbot",
    description="MVP API for Smart India Hackathon 2025 groundwater chatbot",
    version="0.1.0",
    lifespan=lifespan
)

# Allow frontend access (update for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str
    lang: str = "en"


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log basic request info for debugging during SIH testing.
    """
    print(f"[REQUEST] {request.method} {request.url}")
    response = await call_next(request)
    print(f"[RESPONSE] Status: {response.status_code}")
    return response


@app.get("/")
def root():
    return {"message": "AI INGRES Chatbot API running"}


@app.get("/data/query")
def data_query(
    state: str = Query(None, description="Name of the state to filter by"),
    year: str = Query(None, description="Year to filter by"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max number of records to return")
):
    if not data_cache:
        raise HTTPException(status_code=500, detail="Data not loaded")

    results = [
        row for row in data_cache
        if (not state or row.get("state", "").casefold() == state.casefold())
        and (not year or row.get("year", "") == year)
    ]

    return {
        "total": len(results),
        "results": results[skip: skip + limit]
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = handle_query(request.query, request.lang)
        return response
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=f"Initialization error: {str(re)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
