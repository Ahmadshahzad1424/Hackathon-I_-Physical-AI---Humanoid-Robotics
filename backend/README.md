# RAG Book Embeddings Pipeline

This project implements a pipeline to crawl Docusaurus documentation sites, generate embeddings using Cohere, and store them in Qdrant Cloud for RAG (Retrieval Augmented Generation) applications.

## Prerequisites

- Python 3.11+
- `uv` package manager (optional, for faster dependency management)
- Cohere API key
- Qdrant Cloud account and API key

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

### 3. Install dependencies with uv (recommended) or pip
```bash
# Using uv (recommended for faster installation)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Or using pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the backend directory:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys and configuration:
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

## Usage

### Run the full pipeline
```bash
cd backend
python main.py
```

### Configuration Options
- `CHUNK_SIZE`: Size of text chunks for embedding (default: 512)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)
- `EMBEDDING_MODEL`: Cohere model to use (default: embed-english-v3.0)
- `QDRANT_COLLECTION_NAME`: Name of Qdrant collection (default: book_embeddings)

## Architecture

The pipeline consists of the following components:

1. **Crawler** (`crawler.py`): Fetches and extracts content from Docusaurus URLs
2. **Chunker** (`chunker.py`): Splits content into manageable chunks for embedding
3. **Embedding Service** (`embedding_service.py`): Generates embeddings using Cohere API
4. **Qdrant Service** (`qdrant_service.py`): Stores embeddings in Qdrant Cloud
5. **Job Manager** (`job_manager.py`): Tracks pipeline execution progress
6. **Pipeline** (`pipeline.py`): Orchestrates the entire process
7. **Configuration** (`config.py`): Handles environment variables and settings
8. **Models** (`models.py`): Defines data structures for the pipeline

## Environment Variables

- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL to your Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for Qdrant Cloud access
- `VERCEL_URLS`: Comma-separated list of Docusaurus site URLs to crawl
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection to store embeddings
- `CHUNK_SIZE`: Maximum characters per text chunk (default: 512)
- `CHUNK_OVERLAP`: Number of characters to overlap between chunks (default: 50)
- `EMBEDDING_MODEL`: Cohere model to use for embeddings (default: embed-english-v3.0)

## Troubleshooting

1. **API Key Issues**: Ensure your Cohere and Qdrant API keys are valid and have the necessary permissions
2. **URL Access Issues**: Verify that the URLs in `VERCEL_URLS` are publicly accessible
3. **Memory Issues**: For large documentation sets, consider reducing the chunk size or processing in smaller batches

## Development

To run with custom URLs:
```bash
python main.py
```

The pipeline will use the URLs specified in the `VERCEL_URLS` environment variable.