
#  RAG Demo – PDF Q&A (FastAPI + Together + Qdrant)

This project demonstrates a simple **RAG (Retrieval-Augmented Generation)** pipeline:

* Upload a PDF (Terms & Conditions / Agreement)
* Store content as embeddings in Qdrant (vector DB)
* Ask natural language questions
* Get answers grounded in the PDF content

---

## ✅ Prerequisites

Make sure you have:

* Python **3.10+** (tested with 3.11 / 3.13)
* Git (optional, if cloning repo)
* A Together.ai API key
* A Qdrant Cloud URL + API key (or local Qdrant if configured)

---

## Setup

### 1️⃣ Clone repo (if applicable)

```bash
git clone <your-repo-url>
cd rag-demo
```

Or unzip the project and `cd` into the folder.

---

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
# OR
.venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

---

## ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 How to Test (Swagger UI)

Open:

 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

### 1️⃣ Ingest PDF

Endpoint:

```
POST /ingest
```

* Upload a PDF file (Terms & Conditions / Agreement)
* This will:

  * Read PDF
  * Chunk text
  * Create embeddings
  * Store in Qdrant

Response:

```json
{
  "status": "ok",
  "chunks": 12
}
```

---

### 2️⃣ Search (Optional – Debug)

Endpoint:

```
POST /search?query=Who can use PhonePe services?
```

This returns top matching chunks from the document.

---

### 3️⃣ Ask Question (Main Endpoint)

Endpoint:

```
POST /answer?query=Who can use PhonePe services?
```

Response:

```json
"To use PhonePe services, you must be legally eligible to enter a contract under Indian law and have a valid mobile number and bank account."
```

This answer is **grounded in the uploaded PDF**.

---

## 🧠 What This Demo Shows

* How embeddings work
* How vector search retrieves relevant document parts
* How LLM answers using retrieved context
* No hallucination (answer only from PDF content)

---

