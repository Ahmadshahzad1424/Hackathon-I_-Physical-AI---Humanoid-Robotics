# Data Model: URL Ingestion & Embedding Pipeline

## Entity: CrawledPage
- **id**: str (auto-generated UUID)
- **url**: str (source URL of the page)
- **title**: str (page title from HTML)
- **content**: str (cleaned text content)
- **metadata**: dict (additional page metadata like headings, links)
- **created_at**: datetime (timestamp of crawling)
- **updated_at**: datetime (timestamp of last update)

**Validation rules**:
- url must be a valid URL format
- content must not be empty after cleaning
- title must not be empty

## Entity: TextChunk
- **id**: str (auto-generated UUID)
- **page_id**: str (foreign key to CrawledPage)
- **content**: str (chunked text content)
- **chunk_index**: int (position of chunk in original page)
- **token_count**: int (number of tokens in chunk)
- **embedding**: list[float] (vector representation, optional until embedded)
- **created_at**: datetime (timestamp of chunking)

**Validation rules**:
- content must not exceed maximum token length for embedding model
- chunk_index must be non-negative
- token_count must be positive

## Entity: EmbeddingRecord
- **id**: str (auto-generated UUID)
- **chunk_id**: str (foreign key to TextChunk)
- **vector**: list[float] (embedding vector from Cohere)
- **collection_name**: str (Qdrant collection name)
- **payload**: dict (metadata for Qdrant including source URL, title)
- **created_at**: datetime (timestamp of embedding)

**Validation rules**:
- vector must have consistent dimensions across records
- collection_name must follow Qdrant naming conventions
- payload must include required metadata fields

## Entity: ProcessingJob
- **id**: str (auto-generated UUID)
- **status**: str (PENDING, IN_PROGRESS, COMPLETED, FAILED)
- **urls**: list[str] (list of URLs to process)
- **processed_count**: int (number of URLs processed)
- **total_count**: int (total number of URLs to process)
- **error_message**: str (error details if failed)
- **created_at**: datetime (timestamp of job creation)
- **completed_at**: datetime (timestamp of job completion, optional)

**Validation rules**:
- status must be one of the allowed values
- processed_count must not exceed total_count
- error_message only present when status is FAILED

## Relationships
- ProcessingJob 1 -> * CrawledPage (one job can result in many pages)
- CrawledPage 1 -> * TextChunk (one page can be chunked into many pieces)
- TextChunk 1 -> 1 EmbeddingRecord (one chunk maps to one embedding record)

## State Transitions
- ProcessingJob: PENDING -> IN_PROGRESS -> COMPLETED/FAILED