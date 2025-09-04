import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Remove OpenAI dependency
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY is not set in environment variables.")

PDF_DIR = "backend/app/data/docs/methodology" 
INDEX_PATH = "backend/app/data/embeddings" 

def load_pdfs(pdf_dir):
    """Load all PDFs in the given folder into LangChain Documents."""
    if not os.path.exists(pdf_dir):
        print(f"[WARNING] Directory {pdf_dir} does not exist. Creating it...")
        os.makedirs(pdf_dir, exist_ok=True)
        print(f"[INFO] Please add PDF files to {pdf_dir} and run again.")
        return []
    
    all_docs = []
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print(f"[WARNING] No PDF files found in {pdf_dir}")
        print(f"[INFO] Please add PDF files to {pdf_dir} and run again.")
        return []
    
    for filename in pdf_files:
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

    if not documents:
        print("[ERROR] No documents to process. Exiting.")
        return

    print(f"[INFO] Loaded {len(documents)} document chunks before splitting.")

    # Split text into smaller chunks for better search accuracy
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)

    print(f"[INFO] Split into {len(split_docs)} chunks.")

    print("[INFO] Creating embeddings and FAISS index...")
    # Use free HuggingFace embeddings instead of OpenAI
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    os.makedirs(INDEX_PATH, exist_ok=True)
    vectorstore.save_local(INDEX_PATH)

    print(f"[SUCCESS] FAISS index saved to {INDEX_PATH}")

if __name__ == "__main__":
    build_faiss_index()