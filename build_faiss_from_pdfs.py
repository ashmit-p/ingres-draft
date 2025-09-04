import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

PDF_DIR = "data/docs/methodology"   
INDEX_PATH = "data/embeddings"      

def load_pdfs(pdf_dir):
    """Load all PDFs in the given folder into LangChain Documents."""
    all_docs = []
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            print(f"[INFO] Loading {pdf_path}...")
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            # Add filename to metadata for citations
            for doc in docs:
                doc.metadata["source"] = filename
            all_docs.extend(docs)
    return all_docs

def build_faiss_index():
    print("[INFO] Loading PDF documents...")
    documents = load_pdfs(PDF_DIR)

    print(f"[INFO] Loaded {len(documents)} document chunks before splitting.")

    # Split text into smaller chunks for better search accuracy
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)

    print(f"[INFO] Split into {len(split_docs)} chunks.")

    print("[INFO] Creating embeddings and FAISS index...")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    os.makedirs(INDEX_PATH, exist_ok=True)
    vectorstore.save_local(INDEX_PATH)

    print(f"[SUCCESS] FAISS index saved to {INDEX_PATH}")

if __name__ == "__main__":
    build_faiss_index()
