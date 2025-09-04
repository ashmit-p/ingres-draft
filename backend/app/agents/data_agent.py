import pandas as pd
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "reports.csv")

def handle_data_query(query: str, lang: str = "en"):
    """
    Mock data query handler.
    For MVP: loads static CSV and returns filtered results.
    """
    try:
        df = pd.read_csv(DATA_FILE)

        matched_state = None
        for state in df["State"].unique():
            if state.lower() in query.lower():
                matched_state = state
                break

        if matched_state:
            data = df[df["State"] == matched_state].to_dict(orient="records")
            return {
                "type": "data",
                "query": query,
                "language": lang,
                "state": matched_state,
                "results": data,
                "citations": ["CGWB National Compilation Report (2022)"]
            }
        else:
            return {
                "type": "data",
                "query": query,
                "language": lang,
                "message": "No matching state found in dataset.",
                "citations": []
            }
    except Exception as e:
        return {"error": str(e)}
