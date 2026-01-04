# Data Model: RAG Agent with OpenAI SDK

## Entities

### AgentSession
- **session_id**: string (UUID) - Unique identifier for each conversation session
- **created_at**: datetime - Timestamp when session was created
- **updated_at**: datetime - Timestamp when session was last updated
- **conversation_context**: dict - Stores the conversation history and context
- **metadata**: dict - Additional session metadata

**Validation Rules**:
- session_id must be a valid UUID
- created_at must be in the past
- updated_at must be >= created_at

**State Transitions**:
- Created → Active (when first query is processed)
- Active → Ended (when session is closed)

### RetrievalRequest
- **request_id**: string (UUID) - Unique identifier for each retrieval request
- **session_id**: string - Reference to the parent session
- **query_text**: string - Original query from user
- **timestamp**: datetime - When the request was made
- **retrieved_chunks**: list - List of retrieved content chunks
- **retrieval_metadata**: dict - Additional metadata about the retrieval

**Validation Rules**:
- request_id must be a valid UUID
- session_id must reference an existing session
- query_text must not be empty
- retrieved_chunks must be an array of content chunks

### RetrievedChunk
- **chunk_id**: string - ID of the chunk in Qdrant
- **content**: string - The actual content text
- **source_url**: string - URL where the content originated
- **score**: float - Similarity score from vector search
- **page_id**: string - ID of the original page
- **chunk_index**: integer - Position of the chunk in the original document

**Validation Rules**:
- score must be between 0 and 1
- chunk_index must be non-negative
- content must not be empty

### AgentResponse
- **response_id**: string (UUID) - Unique identifier for each response
- **session_id**: string - Reference to the parent session
- **request_id**: string - Reference to the original request
- **content**: string - The agent's response content
- **timestamp**: datetime - When the response was generated
- **citations**: list - List of source citations used in the response
- **response_metadata**: dict - Additional response metadata

**Validation Rules**:
- response_id must be a valid UUID
- session_id must reference an existing session
- content must not be empty
- citations must reference actual retrieved chunks