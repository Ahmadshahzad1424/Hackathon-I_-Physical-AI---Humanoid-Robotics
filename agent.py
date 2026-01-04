#!/usr/bin/env python3
"""
RAG Agent using OpenAI Agents SDK

This module implements an AI agent that uses the OpenAI Agents SDK to answer questions
about book content using retrieved information from Qdrant vector database.
"""

import os
import logging
from typing import Optional, Dict, Any, List
from agents import Agent, Runner, function_tool
from backend.qdrant_service import QdrantService
from backend.embedding_service import EmbeddingService
from backend.config import Config
from backend.models import AgentSession, RetrievalRequest, RetrievedChunk, AgentResponse
import uuid


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@function_tool
def retrieval_tool(query: str) -> Dict[str, Any]:
    """
    Dedicated retrieval tool function that queries Qdrant, designed to work with OpenAI Agents SDK

    Args:
        query: The query to search for in the documentation

    Returns:
        Dictionary with retrieved content and metadata
    """
    try:
        # Initialize Qdrant service for the tool
        qdrant_service = QdrantService()

        # Use the search_text method from QdrantService
        results = qdrant_service.search_text(query, limit=5)

        retrieved_chunks = []
        for result in results:
            payload = result.get('payload', {})
            chunk = {
                "id": result.get('id'),
                "content": payload.get('content', ''),
                "source_url": payload.get('source_url', ''),
                "score": result.get('score', 0.0),
                "page_id": payload.get('page_id', ''),
                "chunk_index": payload.get('chunk_index', 0)
            }
            retrieved_chunks.append(chunk)

        logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query: {query}")

        # Check if no relevant content was found
        if not retrieved_chunks:
            logger.info(f"Retrieval tool executed for query: {query}, but no relevant content was found")
            return {
                "retrieved_chunks": [],
                "count": 0,
                "query": query,
                "status": "no_content_found",
                "message": "No relevant content found for the given query"
            }

        # Format the results for the assistant
        result = {
            "retrieved_chunks": retrieved_chunks,
            "count": len(retrieved_chunks),
            "query": query,
            "status": "success"
        }

        logger.info(f"Retrieval tool executed for query: {query}, found {len(retrieved_chunks)} chunks")
        return result

    except Exception as e:
        logger.error(f"Error in retrieval tool for query '{query}': {str(e)}")
        return {
            "retrieved_chunks": [],
            "count": 0,
            "query": query,
            "status": "error",
            "error_message": str(e)
        }


class RAGAgent:
    """
    RAG Agent that uses OpenAI Agents SDK to answer questions using retrieved content
    """

    def __init__(self):
        """
        Initialize the RAG Agent
        """
        # Initialize Qdrant service
        self.qdrant_service = QdrantService()

        # Initialize embedding service
        self.embedding_service = EmbeddingService()

        # Check for OpenAI API key
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.warning("OPENAI_API_KEY environment variable is not set")

        # Create the agent with retrieval tool using OpenAI Agents SDK
        self.agent = Agent(
            name="RAG Book Content Assistant",
            instructions="You are a helpful assistant that answers questions based on retrieved content from book documentation. Always base your answers on the information provided by the retrieval tool. If the retrieved content doesn't answer the question, say so clearly.",
            tools=[retrieval_tool],
            model="gpt-4-turbo"  # Specify the model to use
        )

        logger.info("RAG Agent initialized successfully")

    def query(self, question: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Query the agent with a question

        Args:
            question: The question to ask
            session_id: Optional session ID for conversation context

        Returns:
            Dictionary containing the response and metadata
        """
        # Input validation
        if not question or not isinstance(question, str):
            logger.error(f"Invalid question provided: {question}")
            return {
                "response": "Please provide a valid question.",
                "session_id": session_id,
                "retrieved_chunks": [],
                "citations": [],
                "status": "error",
                "error_message": "Question must be a non-empty string"
            }

        # Trim whitespace and check for empty question after trimming
        question = question.strip()
        if not question:
            logger.error("Empty question provided after trimming")
            return {
                "response": "Please provide a valid question.",
                "session_id": session_id,
                "retrieved_chunks": [],
                "citations": [],
                "status": "error",
                "error_message": "Question cannot be empty"
            }

        # Check for maximum question length to prevent abuse
        if len(question) > 1000:
            logger.error(f"Question too long: {len(question)} characters")
            return {
                "response": "Your question is too long. Please keep it under 1000 characters.",
                "session_id": session_id,
                "retrieved_chunks": [],
                "citations": [],
                "status": "error",
                "error_message": "Question exceeds maximum length of 1000 characters"
            }

        logger.info(f"Processing query: {question}")

        try:
            # Use the Runner to execute the agent with the question
            from agents.extensions.memory import AdvancedSQLiteSession
            from agents import Runner

            # Create a session for conversation management if session_id is provided
            if session_id:
                session = AdvancedSQLiteSession(
                    session_id=session_id,
                    db_path="conversations.db",
                    create_tables=True
                )
            else:
                # Generate a new session ID if none provided
                session_id = str(uuid.uuid4())
                session = AdvancedSQLiteSession(
                    session_id=session_id,
                    db_path="conversations.db",
                    create_tables=True
                )

            # Run the agent with the question
            result = Runner.run_sync(self.agent, question, session=session)

            # Extract the response from the result
            response_text = result.final_output if hasattr(result, 'final_output') else str(result)

            # Extract retrieved chunks from the tool execution if available
            retrieved_chunks = []
            citations = []

            # For now, return a basic response - in a real implementation,
            # we would extract the retrieved chunks from the tool execution
            formatted_response = {
                "response": response_text,
                "session_id": session_id,
                "retrieved_chunks": retrieved_chunks,
                "citations": citations,
                "status": "success"
            }

            return formatted_response

        except Exception as e:
            logger.error(f"Error processing query '{question}' in session {session_id}: {str(e)}")
            return {
                "response": "I'm sorry, I encountered an error processing your request. Please try again.",
                "session_id": session_id,
                "retrieved_chunks": [],
                "citations": [],
                "status": "error",
                "error_message": str(e)
            }

    def start_session(self) -> str:
        """
        Start a new conversation session

        Returns:
            Session ID for the new session
        """
        session_id = str(uuid.uuid4())
        logger.info(f"Started new session with ID: {session_id}")
        return session_id

    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get the conversation history for a session

        Args:
            session_id: ID of the session

        Returns:
            List of conversation messages
        """
        # In the OpenAI Agents SDK, conversation history is managed by the session
        # For now, return an empty list - in a real implementation, we would extract
        # the history from the session store
        logger.warning("Conversation history retrieval not fully implemented in this version")
        return []

    def get_session_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the full context for a session including conversation history and metadata

        Args:
            session_id: ID of the session

        Returns:
            Session context or None if session not found
        """
        # In the OpenAI Agents SDK, session context is managed by the session store
        # For now, return a basic context - in a real implementation, we would extract
        # the context from the session store
        logger.warning("Session context retrieval not fully implemented in this version")
        return {
            "session_id": session_id,
            "conversation_context": {},
            "metadata": {}
        }


def main():
    """
    Main function to demonstrate the RAG Agent
    """
    print("RAG Agent Demo")
    print("==============")

    try:
        agent = RAGAgent()
        print("Agent initialized successfully")

        # Example query
        response = agent.query("What is ROS 2?")
        print(f"Response: {response}")

    except Exception as e:
        logger.error(f"Error initializing or running agent: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()