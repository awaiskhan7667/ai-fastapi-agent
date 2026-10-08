# AI FastAPI Agent

An AI-powered backend built with **FastAPI**, **RAG**, **LLM tool calling**, **LangGraph**, and **Docker**.
The project demonstrates how to build and evaluate an AI agent that can answer questions, retrieve information from PDFs, and use tools such as weather and calculator functions.

## 🚀 Features

* FastAPI REST API
* OpenAI LLM integration
* PDF-based RAG
* FAISS vector search
* Sentence Transformers embeddings
* LLM tool calling
* Weather tool
* Calculator tool
* LangGraph agent workflow
* Basic agent evaluation
* SQLite database
* JWT authentication
* Dockerized application
* Swagger API documentation

## 🏗️ Architecture

```text
User
  ↓
FastAPI
  ↓
AI Service
  ↓
LLM
  ↓
┌─────────────────────┐
│                     │
RAG                Tools
│                     │
PDF → Chunks      Weather
     ↓             Calculator
Embeddings
     ↓
FAISS
└─────────────────────┘
  ↓
Response
```

## 📁 Project Structure

```text
ai-fastapi-agent/
│
├── main.py
├── database.py
├── auth.py
├── config.py
├── Dockerfile
├── requirements.txt
├── .gitignore
├── .dockerignore
│
├── models/
│   ├── student.py
│   ├── student_db.py
│   └── ai.py
│
├── router/
│   ├── students.py
│   └── ai.py
│
├── services/
│   ├── student_service.py
│   ├── ai_services.py
│   ├── rag_service.py
│   ├── tools.py
│   └── agent.py
│
└── documents/
    └── sample.pdf
```

## 🛠️ Technologies

* Python
* FastAPI
* OpenAI API
* LangChain
* LangGraph
* FAISS
* Sentence Transformers
* SQLAlchemy
* SQLite
* JWT
* Docker
* Git & GitHub

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/awaiskhan7667/ai-fastapi-agent.git
cd ai-fastapi-agent
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

**Never commit your `.env` file to GitHub.**

## ▶️ Run Locally

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Open Swagger:

```text
http://localhost:8000/docs
```

## 🐳 Run with Docker

Build the Docker image:

```bash
docker build -t ai-fastapi .
```

Run the container:

```bash
docker run --env-file .env -p 8000:8000 ai-fastapi
```

Then open:

```text
http://localhost:8000/docs
```

## 🤖 AI Agent

The LangGraph agent follows this workflow:

```text
START
  ↓
ANSWER
  ↓
Tool Call?
 ↙      ↘
No      Yes
↓        ↓
END     TOOL
          ↓
        ANSWER
```

The agent can decide when to use available tools and return the final response.

## 🔧 Available Tools

### Weather

Returns weather information for a city.

### Calculator

Supports:

* Addition
* Subtraction
* Multiplication
* Division

The calculator also handles division by zero.

## 📚 RAG

The RAG pipeline follows:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS Index
 ↓
Similarity Search
 ↓
Relevant Context
 ↓
LLM
 ↓
Answer
```

The AI is instructed to answer using the retrieved document context.

## 🧪 Evaluation

The project includes basic evaluation test cases for:

* Mathematical calculations
* Weather queries
* Division by zero
* Expected answer matching

Example:

```text
Question → Expected Answer → Actual Answer → PASS/FAIL
```

## 🎯 Learning Goals

This project was built to practice the core skills required for an **AI Engineer**, including:

* Building AI APIs
* Integrating LLMs
* Retrieval-Augmented Generation
* Vector search
* Tool calling
* Agent workflows
* Evaluation
* Dockerization
* Backend engineering

## 🔮 Future Improvements

* Persistent conversation memory
* Better RAG retrieval
* Streaming responses
* Advanced evaluation
* Production database
* Authentication improvements
* Cloud deployment
* Monitoring and observability

## 👨‍💻 Author

**Awais Khan**

Software Engineer | AI Engineer

GitHub:
https://github.com/awaiskhan7667
