import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "embeddings")

def handle_doc_query(query: str, lang: str = "en"):
    """
    Mock document query handler using prebuilt FAISS index.
    """
    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

        docs = vectorstore.similarity_search(query, k=2)
        return {
            "type": "methodology",
            "query": query,
            "language": lang,
            "answers": [doc.page_content for doc in docs],
            "citations": [doc.metadata.get("source", "GEC-2015 Methodology")] * len(docs)
        }
    except Exception as e:
        return {"error": str(e)}
