from .agents.data_agent import handle_data_query
from .agents.doc_agent import handle_doc_query

def handle_query(query: str, lang: str = "en"):
    """
    Routes the query to either the Data Agent or Document Agent
    based on simple keyword classification.
    For MVP, uses rule-based detection.
    """

    data_keywords = ["water", "recharge", "level", "state", "year", "availability", "table", "statistics"]
    methodology_keywords = ["methodology", "GEC", "calculation", "criteria", "estimation", "rules"]

    # Simple rule-based classification
    if any(kw in query.lower() for kw in data_keywords):
        return handle_data_query(query, lang)
    elif any(kw in query.lower() for kw in methodology_keywords):
        return handle_doc_query(query, lang)
    else:
        # Default fallback
        return handle_doc_query(query, lang)
