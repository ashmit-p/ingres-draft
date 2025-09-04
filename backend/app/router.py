from .agents.data_agent import DataAgent
from .agents.doc_agent import DocAgent

data_agent = None
doc_agent = None


def init_agents():
    """
    Initializes global agent instances.
    Called once from FastAPI lifespan handler.
    """
    global data_agent, doc_agent
    data_agent = DataAgent()
    doc_agent = DocAgent()
    print("[INFO] Agents initialized successfully")


def shutdown_agents():
    """
    Clean up resources on shutdown.
    """
    global data_agent, doc_agent
    data_agent = None
    doc_agent = None
    print("[INFO] Agents cleared on shutdown")


def handle_query(query: str, lang: str = "en"):
    """
    Routes the query to either the Data Agent or Document Agent
    based on simple keyword classification.
    Uses rule-based approach for MVP.
    """
    global data_agent, doc_agent

    if not data_agent or not doc_agent:
        raise RuntimeError("Agents are not initialized")

    data_keywords = ["water", "recharge", "level", "state", "year", "availability", "table", "statistics"]
    methodology_keywords = ["methodology", "GEC", "calculation", "criteria", "estimation", "rules"]

    query_lower = query.lower()

    if any(kw in query_lower for kw in data_keywords):
        return data_agent.handle_query(query, lang)
    elif any(kw in query_lower for kw in methodology_keywords):
        return doc_agent.handle_query(query, lang)
    else:
        return doc_agent.handle_query(query, lang)
