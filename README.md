# IMDB Movie RAG API Using Qdrant Vector Database

A streaming Retrieval-Augmented Generation (RAG) API built with FastAPI that allows users to chat with and search through IMDB movie data. The system uses vector embeddings, Qdrant vector database, and Ollama for local LLM inference to provide intelligent movie recommendations and information.

## 🎬 Features

- **Streaming Chat Interface**: Real-time streaming responses for natural conversations about movies
- **Vector Search**: Semantic search through movie data using embeddings
- **RAG System**: Combines retrieval and generation for context-aware responses
- **Docker Support**: Complete containerized setup with Docker Compose
- **Persistent Storage**: PostgreSQL for chat memory and Qdrant for vector storage
- **Local LLM**: Uses Ollama for local language model inference
- **RESTful API**: Clean API endpoints for both streaming and non-streaming requests

## 📊 Data Source

This project uses the [IMDB Top 1000 Movies Dataset](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows) which contains:

- **1,000 movies** from IMDB's top-rated films
- **Movie metadata** including:
  - Title, Release Year, Runtime, Genre
  - IMDB Rating, Meta Score, Director
  - Cast information (4 main stars)
  - Plot overview and gross earnings
  - Poster links

**Note**: This project is for educational and demonstration purposes. If you plan to use this data commercially, please ensure compliance with IMDB's terms of service and any applicable data usage policies.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- Ollama (for local LLM models)

### Using Docker Compose

1. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start the services**

   ```bash
   docker-compose up -d --build
   ```

3. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/health

### Local Development

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**

   ```bash
   export COLLECTION_NAME="imdb_rating"
   export EMBEDDED_MODEL="llama2"
   export FILE_PATH="src/data/imdb_top_1000.csv"
   export LLM_MODEL="llama2"
   export OLLAMA_API="http://localhost:11434"
   export QDRANT_URL="http://localhost:6333"
   export POSTGRES_HOST="localhost"
   export POSTGRES_PORT="5432"
   export POSTGRES_DB="app"
   export POSTGRES_USER="your_user"
   export POSTGRES_PASSWORD="your_password"
   ```

3. **Start Qdrant and PostgreSQL**

   ```bash
   docker-compose up qdrant postgres -d
   ```

4. **Start Ollama**

   ```bash
   ollama serve
   ollama pull llama2
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 📡 API Endpoints

### Chat Endpoints

- `POST /api/chat/stream` - Streaming chat with the RAG system
- `POST /api/chat` - Non-streaming chat endpoint

### Search Endpoints

- `POST /api/search/stream` - Streaming vector search
- `POST /api/search` - Non-streaming search endpoint

### Utility Endpoints

- `GET /api/health` - Health check

### Example Usage

#### Streaming Chat

```bash
curl -X POST "http://localhost:8000/api/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the best action movies from the 2000s?",
    "user_id": "user123"
  }'
```

#### Vector Search

```bash
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Christopher Nolan movies",
    "limit": 5
  }'
```

## 🏛️ Project Structure

```
imdb-movie-rag/
├── src/
│   ├── api/                 # FastAPI routes and schemas
│   ├── config/              # Configuration management
│   ├── core/                # Core functionality (indexing, models)
│   ├── data/                # IMDB dataset
│   ├── pipeline/            # Data processing pipeline
│   ├── services/            # Chat engine service
│   └── utils/               # Utility functions
├── .env_sample              # .env example
├── docker-compose.yaml      # Docker services configuration
├── Dockerfile              # Application container
├── main.py                 # Application entry point
└── requirements.txt        # Python dependencies
```

**Note**: This project is for educational and demonstration purposes. Please ensure compliance with data usage policies when using IMDB data commercially.
