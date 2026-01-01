# Feature Specification: RAG Book Embeddings

## Overview
Deploy book URLs, generate embeddings, and store them in a vector database

Target audience: Developers integrating RAG with documentation websites
Focus: Reliable ingestion, embedding, and storage of book content for retrieval

## User Scenarios & Testing

### Scenario 1: Documentation Ingestion
As a developer integrating RAG with documentation websites, I want to automatically crawl and clean public Docusaurus URLs so that I can extract relevant content for vector search.

**Acceptance Criteria:**
- System can crawl all public URLs from a deployed Docusaurus site
- Content is cleaned of HTML tags, navigation elements, and other non-content text
- Text extraction preserves meaningful content while removing boilerplate

### Scenario 2: Text Embedding
As a developer, I want to chunk and embed the extracted text using Cohere models so that I can store and retrieve relevant content efficiently.

**Acceptance Criteria:**
- Text is properly chunked into meaningful segments
- Cohere embeddings are generated for each text chunk
- Embeddings maintain semantic meaning of the original content

### Scenario 3: Vector Storage
As a developer, I want to store embeddings in Qdrant vector database so that I can perform efficient similarity searches.

**Acceptance Criteria:**
- Embeddings are successfully stored in Qdrant
- Vector indexes are properly created for efficient search
- Data is properly indexed with metadata for retrieval

### Scenario 4: Search Validation
As a developer, I want to test vector search functionality so that I can verify the system returns relevant chunks for test queries.

**Acceptance Criteria:**
- Vector search returns relevant content for test queries
- Search results are ranked by similarity
- Response time is acceptable for production use

## Functional Requirements

### FR-1: URL Crawling
The system SHALL crawl all public URLs from deployed Docusaurus sites.
- The crawler SHALL follow internal links to discover all pages
- The crawler SHALL respect robots.txt and crawl delays
- The crawler SHALL handle redirects and broken links gracefully

### FR-2: Content Cleaning
The system SHALL clean crawled content to extract meaningful text.
- HTML tags SHALL be removed while preserving text content
- Navigation, footer, and sidebar content SHALL be excluded
- Code blocks and special formatting SHALL be preserved appropriately

### FR-3: Text Chunking
The system SHALL chunk cleaned text into meaningful segments.
- Text chunks SHALL be of appropriate size for embedding models
- Chunking SHALL preserve context and semantic meaning
- Overlapping boundaries SHALL be handled to maintain context

### FR-4: Embedding Generation
The system SHALL generate embeddings using Cohere models.
- Cohere API integration SHALL be properly configured
- Embeddings SHALL be generated for each text chunk
- Error handling SHALL be implemented for API failures

### FR-5: Vector Storage
The system SHALL store embeddings in Qdrant vector database.
- Qdrant connection SHALL be established using provided credentials
- Embeddings SHALL be stored with appropriate metadata
- Vector indexes SHALL be created for efficient search

### FR-6: Search Validation
The system SHALL provide functionality to test vector search.
- Test queries SHALL be executed against the vector database
- Results SHALL be ranked by similarity
- Performance metrics SHALL be available for validation

## Success Criteria

### Quantitative Metrics
- 95% of public Docusaurus URLs are successfully crawled and processed
- Text embedding process completes within 10 minutes per 100 pages
- Vector search returns results within 500ms response time
- 90% of test queries return relevant content in top 3 results

### Qualitative Measures
- Content extraction preserves meaning and context
- Embeddings capture semantic relationships in the text
- System handles various Docusaurus site structures
- Error handling provides clear feedback for failures

## Key Entities

### CrawledContent
- URL: Source URL of the content
- Title: Page title
- Text: Cleaned text content
- Metadata: Additional page metadata

### TextChunk
- Id: Unique identifier for the chunk
- Content: Text content of the chunk
- SourceUrl: URL where the chunk originated
- Embedding: Vector representation of the chunk

### VectorRecord
- Id: Unique identifier for the record
- Vector: Embedding vector
- Payload: Metadata associated with the vector
- Collection: Qdrant collection name

## Constraints

### Technical Constraints
- Tech stack: Python, Cohere Embeddings, Qdrant (Cloud Free Tier)
- Data source: Deployed Vercel URLs only
- Format: Modular scripts with clear config/env handling
- Timeline: Complete within 3-5 tasks

### Scope Constraints
- Not building retrieval or ranking logic
- Not building agent or chatbot logic
- Not building frontend or FastAPI integration
- Not building user authentication or analytics

## Assumptions

1. Deployed Docusaurus sites are publicly accessible without authentication
2. Cohere API is available and properly configured with valid API keys
3. Qdrant cloud instance is properly configured and accessible
4. Docusaurus sites follow standard structure for content extraction
5. Network connectivity is available for external API calls

## Dependencies

1. Cohere API access and credentials
2. Qdrant vector database instance
3. Publicly deployed Docusaurus URLs
4. Python environment with required dependencies