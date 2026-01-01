# Quickstart: URL Ingestion & Embedding Pipeline

## Prerequisites
- Python 3.11+
- Cohere API key
- Qdrant Cloud instance and API key
- `uv` package manager (or pip)

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Navigate to backend directory
```bash
cd backend
```

### 3. Install dependencies with uv
```bash
# Install uv if you don't have it
pip install uv

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the backend directory:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
VERCEL_URLS=https://your-docusaurus-site.com/docs/,https://another-site.com/docs/
QDRANT_COLLECTION_NAME=book_embeddings
CHUNK_SIZE=512
CHUNK_OVERLAP=50
EMBEDDING_MODEL=embed-english-v3.0
```

### 5. Run the ingestion pipeline
```bash
cd backend
python main.py
```

## Usage

The main pipeline function will:
1. Crawl the specified Docusaurus URLs
2. Clean and extract text content
3. Chunk the text into manageable pieces
4. Generate embeddings using Cohere
5. Store embeddings in Qdrant Cloud
6. Track job progress and status

## Configuration

### Environment Variables
- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL to your Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for Qdrant Cloud access
- `VERCEL_URLS`: Comma-separated list of Docusaurus site URLs to crawl
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection to store embeddings
- `CHUNK_SIZE`: Maximum characters per text chunk (default: 512)
- `CHUNK_OVERLAP`: Number of characters to overlap between chunks (default: 50)
- `EMBEDDING_MODEL`: Cohere model to use for embeddings (default: embed-english-v3.0)
- `MAX_RETRIES`: Maximum number of retries for failed operations (default: 3)
- `DELAY_BETWEEN_RETRIES`: Delay in seconds between retries (default: 1)