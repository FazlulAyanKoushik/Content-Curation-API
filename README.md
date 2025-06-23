# 🚀 AI-Powered Content Curation API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![LangChain](https://img.shields.io/badge/LangChain-00A67E?style=for-the-badge)](https://python.langchain.com/)

A FastAPI-based service for content management with AI-powered analysis features including summarization, sentiment analysis, and topic extraction.

## Features

- **User Management**: JWT authentication with role-based access (Public, User, Admin)
- **Content CRUD**: Create, read, update, and delete content items
- **AI Analysis**:
  - Automatic summarization
  - Sentiment analysis (positive/negative/neutral)
  - Topic extraction
- **Search & Recommendations**:
  - Public content search
  - Personalized recommendations
- **Dockerized**: Easy deployment with PostgreSQL database

## Tech Stack

- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **AI**: LangChain + GROQ API
- **Auth**: JWT tokens
- **Containerization**: Docker

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/FazlulAyanKoushik/Content-Curation-API.git
   cd Content-Curation-API
   


## API Endpoints

| Method | Endpoint                     | Description                  | Auth Required |
|--------|------------------------------|------------------------------|---------------|
| POST   | `/accounts/register`             | User registration            | No            |
| POST   | `/accounts/login`                | User login                   | No            |
| POST   | `/content`                   | Create new content           | Yes           |
| GET    | `/content/public`            | Browse public content        | No            |
| GET    | `/search/public`             | Search public content        | No            |
| POST   | `/ai/analyze/{content_id}`   | Run AI analysis              | Yes           |


# Strategic Enhancements Roadmap

---

## 🏗️ Architectural Improvements

### Real-time Processing Pipeline

- **Kafka/RabbitMQ** for asynchronous analysis job orchestration.
- **Dedicated GPU workers** to handle heavy machine learning (ML) workloads.

```bash
# Example command to spin up GPU-enabled services
docker-compose -f docker-compose.gpu.yml up
```

🔍 Hybrid Search
Combining vector-based semantic search with traditional keyword-based search for enhanced relevance.

# Pseudocode for vector + keyword hybrid search
```bash
results = vector_db.semantic_search(query) + \
          postgres.full_text_search(query)
```

# 🚀 🧠 AI/ML Enhancements
| Technique         | Implementation Detail                   | Expected Impact        |
| ----------------- | --------------------------------------- | ---------------------- |
| Model Ensembling  | Combine Groq + OpenAI model outputs     | +15% accuracy          |
| Active Learning   | Use user feedback for retraining models | Continuous improvement |
| Cost Optimization | Route short texts to smaller models     | 40% cost reduction     |
