# AI INGRES Chatbot (MVP)

An AI-driven chatbot to provide **groundwater data** and **GEC-2015 methodology answers** for the **Smart India Hackathon 2025**.

---

## Project Structure

```
backend/
	app/
		agents/         # Data and document agents
		data/           # Data files and embeddings
		tests/          # Unit tests
		utils/          # Utility modules
		main.py         # FastAPI app entry point
		router.py       # API routes
		config.py       # Configuration
	requirements.txt  # Python dependencies
	Dockerfile        # Backend container config
frontend/           # Frontend application
```

## Getting Started (Backend)

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/ingres-draft.git
cd ingres-draft/backend
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv .venv
source .venv/Scripts/activate  # On Windows Bash
```

### 3. Install Dependencies
Add `fastapi` and `uvicorn` to `requirements.txt` if not present:
```
fastapi
uvicorn
```
Then install:
```bash
pip install -r requirements.txt
```

### 4. Run the Backend Server
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Running Tests
```bash
pytest app/tests/
```

## Docker Usage
Build and run the backend using Docker Compose:
```bash
docker-compose up --build
```

## Contributing
Pull requests and issues are welcome! Please follow standard Python and frontend best practices.

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

