# RAG Agent Documentation

## Overview
The RAG (Retrieval-Augmented Generation) Agent is an AI assistant that answers questions about book content using retrieved information from a Qdrant vector database. The agent uses OpenAI's Assistant API to process queries and retrieve relevant content to generate accurate responses.

## Features
- Question answering based on retrieved book content
- Conversation context management with session support
- Dedicated retrieval tool for querying Qdrant
- Error handling and input validation
- Logging for debugging and monitoring

## Setup

### Prerequisites
- Python 3.8+
- OpenAI API key
- Qdrant Cloud URL and API key
- Cohere API key (for embeddings)

### Environment Variables
Create a `.env` file with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
```

### Installation
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```python
from agent import RAGAgent

# Initialize the agent
agent = RAGAgent()

# Ask a question
response = agent.query("What is ROS 2?")
print(response["response"])
```

### Session Management
```python
# Start a new session
session_id = agent.start_session()

# Ask questions within the session
response1 = agent.query("What is ROS 2?", session_id)
response2 = agent.query("What are its main features?", session_id)  # Follow-up question

# Get conversation history
history = agent.get_conversation_history(session_id)
print(f"Conversation has {len(history)} messages")

# End the session
agent.end_session(session_id)
```

### Direct Tool Usage
```python
# Use the retrieval tool directly
result = agent.retrieval_tool("ROS 2 concepts")
print(f"Found {result['count']} relevant chunks")
```

## API Reference

### RAGAgent Class

#### `__init__()`
Initializes the RAG Agent with OpenAI, Qdrant, and embedding services.

#### `query(question: str, session_id: Optional[str] = None) -> Dict[str, Any]`
Processes a question and returns a response with retrieved content.

**Parameters:**
- `question`: The question to ask (max 1000 characters)
- `session_id`: Optional session ID to maintain conversation context

**Returns:**
- `response`: The agent's response text
- `session_id`: The session ID used
- `thread_id`: The OpenAI thread ID
- `retrieved_chunks`: List of retrieved content chunks
- `citations`: List of source citations
- `status`: "success" or "error"
- `error_message`: Error details if status is "error"

#### `start_session() -> str`
Starts a new conversation session.

**Returns:** Session ID for the new session.

#### `end_session(session_id: str) -> bool`
Ends a conversation session.

**Parameters:**
- `session_id`: The ID of the session to end

**Returns:** True if successful, False otherwise.

#### `get_conversation_history(session_id: str) -> List[Dict[str, Any]]`
Gets the conversation history for a session.

**Parameters:**
- `session_id`: The session ID

**Returns:** List of conversation messages.

#### `retrieval_tool(query: str) -> Dict[str, Any]`
Directly retrieves content from Qdrant.

**Parameters:**
- `query`: The query to search for

**Returns:**
- `retrieved_chunks`: List of retrieved content chunks
- `count`: Number of chunks retrieved
- `query`: The original query
- `status`: "success", "no_content_found", or "error"
- `message`: Additional message when no content is found
- `error_message`: Error details if status is "error"

## Error Handling

The agent handles various error scenarios:
- Invalid or empty questions
- Questions that are too long (>1000 characters)
- API connection failures
- No relevant content found in Qdrant
- General system errors

## Logging
The agent logs important events and errors to help with debugging and monitoring. Logs are output at the INFO level by default.

## Testing
Run the tests using:
```bash
python -m pytest tests/
```

Or run specific test files:
```bash
python tests/test_agent.py
python tests/test_retrieval.py
```