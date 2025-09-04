import pandas as pd
import os

class DataAgent:
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(__file__), "..", "data", "reports.csv")
        self.df = None
        self._load_data()

    def _load_data(self):
        try:
            self.df = pd.read_csv(self.data_file)
            print(f"[INFO] DataAgent loaded {len(self.df)} records.")
        except Exception as e:
            print(f"[ERROR] Failed to load CSV: {e}")
            self.df = None

    def handle_query(self, query: str, lang: str = "en"):
        if self.df is None:
            return {"error": "Dataset not loaded"}

        matched_state = None
        for state in self.df["State"].unique():
            if state.lower() in query.lower():
                matched_state = state
                break

        if matched_state:
            data = self.df[self.df["State"] == matched_state].to_dict(orient="records")
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
