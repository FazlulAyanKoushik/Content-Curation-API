# AI-Powered Content Curation API

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
   cd content-curation-api
   


## API Endpoints

| Method | Endpoint                     | Description                  | Auth Required |
|--------|------------------------------|------------------------------|---------------|
| POST   | `/accounts/register`             | User registration            | No            |
| POST   | `/accounts/login`                | User login                   | No            |
| POST   | `/content`                   | Create new content           | Yes           |
| GET    | `/content/public`            | Browse public content        | No            |
| GET    | `/search/public`             | Search public content        | No            |
| POST   | `/ai/analyze/{content_id}`   | Run AI analysis              | Yes           |