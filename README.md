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
