# API Contract: RAG Ingestion Service

## Endpoints

### POST /ingest
**Description**: Start a new ingestion job to crawl URLs, generate embeddings, and store in vector database

**Request**:
```json
{
  "urls": ["https://example.com/docs/intro", "https://example.com/docs/setup"],
  "collection_name": "book_embeddings",
  "chunk_size": 512,
  "chunk_overlap": 50
}
```

**Response**:
```json
{
  "job_id": "uuid-string",
  "status": "PENDING",
  "total_urls": 2,
  "created_at": "2026-01-01T10:00:00Z"
}
```

### GET /ingest/{job_id}
**Description**: Get the status of an ingestion job

**Response**:
```json
{
  "job_id": "uuid-string",
  "status": "IN_PROGRESS",
  "processed_count": 1,
  "total_count": 2,
  "progress_percentage": 50,
  "error_message": null,
  "created_at": "2026-01-01T10:00:00Z",
  "completed_at": null
}
```

### POST /search
**Description**: Search the vector database for relevant content

**Request**:
```json
{
  "query": "How to set up the development environment?",
  "collection_name": "book_embeddings",
  "limit": 5
}
```

**Response**:
```json
{
  "results": [
    {
      "id": "chunk-uuid",
      "content": "To set up the development environment...",
      "source_url": "https://example.com/docs/setup",
      "score": 0.85
    }
  ]
}
```