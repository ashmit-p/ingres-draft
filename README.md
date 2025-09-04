# AI INGRES Chatbot (MVP)

An AI-driven chatbot to provide **groundwater data** and **GEC-2015 methodology answers** for the **Smart India Hackathon 2025**.

---

## 📌 Features
- **Two query types**:
  - 📊 **Data queries** → Returns groundwater stats from a static dataset
  - 📜 **Methodology queries** → Returns GEC-2015 method details using vector search
- **Multilingual-ready** (English/Hindi)
- **Citations included** for all responses
- **Dockerized** for easy deployment

---

## 🛠 Project Structure



# Environment Setup
***
## Python 3.10+
- Virtual environment (venv or conda)
- Install:
    - langchain
    - langgraph
    - fastapi (API backend)
    - uvicorn (server)
    - pydantic (data validation)
    - faiss or chromadb (vector DB)
    - pandas (for CSV parsing)
    - tqdm, requests (data fetching)

***

## Data Collection
- Download CGWB annual reports (PDF, Excel)
- Export important tables to CSV/Parquet
    - **Include:**
        - State-wise groundwater recharge data
        - GEC-2015 methodology document
- Store in `/data` folder

***

## Static Dataset Mock API
- Create a small FastAPI endpoint: `/data/query`
- Serve filtered results from CSV based on parameters (e.g., state, year)
