# LegalAI – Legal Document Summarization & Q&A System

LegalAI is a full-stack AI-powered web application designed to analyze legal documents, generate concise summaries, and answer user queries using Retrieval-Augmented Generation (RAG).  
The project focuses on clean architecture, explainable AI, and a professional UI suitable for final-year academic evaluation.

---

## 🚀 Features

- User Authentication (Login & Register)
- Upload Legal Documents (PDF, DOCX, TXT)
- AI-based Document Summarization
- Ask Natural Language Legal Questions
- Query History with Pagination
- Source-based Answers using RAG
- Dark Woody Themed Professional UI
- Centralized API Layer (no direct API calls in UI components)

---

## 🏗️ Tech Stack

Frontend:
- React.js
- Tailwind CSS
- React Router
- Axios

Backend:
- Spring Boot (REST APIs)
- Python (ML / NLP pipeline)
- FAISS (Vector Search)

AI / ML:
- Sentence Transformers
- Document Chunking & Embeddings
- Retrieval-Augmented Generation (RAG)
- ROUGE Evaluation Metrics

---

## 🔁 Application Flow

1. User registers or logs in
2. Legal document is uploaded
3. Document is processed and indexed
4. User asks a legal question
5. Relevant document chunks are retrieved
6. AI generates answer with sources
7. Queries are stored and shown in history

---

## 🧠 Retrieval-Augmented Generation (RAG)

- Documents are split into semantic chunks
- Chunks are converted into vector embeddings
- FAISS performs similarity search
- Top relevant chunks are retrieved
- LLM generates grounded answers
- Sources are returned for explainability

---


## 🔒 Best Practices

- JWT-based authentication
- Centralized Axios instance
- No direct API calls inside components
- Clean separation of concerns
- Proper loading and error handling

---

## 🧪 Evaluation Metrics

- ROUGE-1, ROUGE-2, ROUGE-L for summarization
- Semantic similarity for retrieval accuracy
- UI usability and consistency

---

## ▶️ Run Frontend Locally

npm install  
npm run dev  

Ensure the backend server is running and the API base URL is configured in axios.js.

---

## 📌 Project Status

- Core features completed
- Frontend and backend integrated
- UI finalized
- Final evaluation in progress

---

## 👤 Author

Shyam ,
Aryan,
Ishwar,
Mangesh
 
Final Year Computer Engineering Student

---

## 📄 License

This project is developed for academic and educational purposes only.
