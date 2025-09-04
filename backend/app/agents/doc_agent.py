import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

class DocAgent:
    def __init__(self):
        self.index_path = os.path.join(os.path.dirname(__file__), "..", "data", "embeddings")
        self.vectorstore = None
        self._load_index()

    def _load_index(self):
        try:
            embeddings = OpenAIEmbeddings()
            self.vectorstore = FAISS.load_local(
                self.index_path,
                embeddings,
                allow_dangerous_deserialization=True
            )
            print("[INFO] DocAgent index loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to load FAISS index: {e}")
            self.vectorstore = None

    def handle_query(self, query: str, lang: str = "en"):
        if self.vectorstore is None:
            return {"error": "FAISS index not loaded"}

        try:
            docs = self.vectorstore.similarity_search(query, k=2)
            return {
                "type": "methodology",
                "query": query,
                "language": lang,
                "answers": [doc.page_content for doc in docs],
                "citations": [doc.metadata.get("source", "GEC-2015 Methodology")] * len(docs)
            }
        except Exception as e:
            return {"error": str(e)}
