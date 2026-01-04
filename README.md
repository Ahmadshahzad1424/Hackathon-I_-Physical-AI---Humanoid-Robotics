# Physical AI & Humanoid Robotics - RAG Agent

This repository contains a Retrieval-Augmented Generation (RAG) agent that answers questions about book content using retrieved information from a Qdrant vector database.

## Features

- Question answering based on retrieved book content using OpenAI Assistant API
- Conversation context management with session support
- Dedicated retrieval tool for querying Qdrant
- Error handling and input validation
- Comprehensive logging for debugging and monitoring

## Prerequisites

- Python 3.8+
- OpenAI API key
- Qdrant Cloud URL and API key
- Cohere API key (for embeddings)

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
```

## Usage

### Running the RAG Agent

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

## Running Tests

Run all tests:

```bash
python -m pytest tests/
```

Run specific test files:

```bash
python tests/test_agent.py
python tests/test_retrieval.py
python tests/test_integration.py
```

## Project Structure

```
.
├── agent.py                    # Main RAG agent implementation
├── requirements.txt            # Python dependencies
├── backend/                  # Backend services
│   ├── qdrant_service.py     # Qdrant integration
│   ├── embedding_service.py  # Embedding generation
│   ├── models.py             # Data models
│   └── config.py             # Configuration
├── docs/                     # Documentation
│   └── rag_agent_api.md      # API documentation
├── tests/                    # Test files
│   ├── test_agent.py         # Basic functionality tests
│   ├── test_retrieval.py     # Retrieval tool tests
│   └── test_integration.py   # Integration tests
└── specs/                    # Specification files
    └── 001-rag-agent/        # RAG agent feature specs
```

## API Documentation

For detailed API documentation, see [docs/rag_agent_api.md](docs/rag_agent_api.md).

## Configuration

The application uses the following environment variables:

- `OPENAI_API_KEY`: OpenAI API key for accessing the Assistant API
- `QDRANT_URL`: URL for the Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant database access
- `COHERE_API_KEY`: API key for generating embeddings
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (default: "book_embeddings")
- `CHUNK_SIZE`: Size of text chunks (default: 512)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)
- `EMBEDDING_MODEL`: Embedding model to use (default: "embed-english-v3.0")
- `MAX_RETRIES`: Maximum number of retries for API calls (default: 3)
- `DELAY_BETWEEN_RETRIES`: Delay between retries in seconds (default: 1)

## Troubleshooting

### Common Issues

1. **API Key Errors**: Make sure all required API keys are set in the `.env` file.
2. **Connection Errors**: Verify that the Qdrant URL and API key are correct.
3. **Rate Limiting**: The application includes rate limiting to handle API limits.

### Logging

The application logs important events and errors. Check the logs if you encounter issues:

```
INFO:root:RAG Agent initialized successfully
INFO:root:Processing query in session new: What is ROS 2?
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`python -m pytest tests/`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

[Add license information here]