#!/usr/bin/env python3
"""
RAG Agent using OpenAI Assistant API

This module implements an AI agent that uses the OpenAI Assistant API to answer questions
about book content using retrieved information from Qdrant vector database.
"""

import os
import logging
import json
from typing import Optional, Dict, Any, List, Callable
from openai import OpenAI
from backend.qdrant_service import QdrantService
from backend.embedding_service import EmbeddingService
from backend.config import Config
from backend.models import AgentSession, RetrievalRequest, RetrievedChunk, AgentResponse


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGAgent:
    """
    RAG Agent that uses OpenAI Assistant API to answer questions using retrieved content
    """

    def __init__(self):
        """
        Initialize the RAG Agent
        """
        # Initialize OpenAI client
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.openai_client = OpenAI(api_key=openai_api_key)

        # Initialize Qdrant service
        self.qdrant_service = QdrantService()

        # Initialize embedding service
        self.embedding_service = EmbeddingService()

        # Create the assistant with retrieval tool
        self.assistant = self._create_assistant()

        logger.info("RAG Agent initialized successfully")

    def _create_assistant(self):
        """
        Create an OpenAI Assistant with retrieval capabilities
        """
        # Create assistant with function that can be used to retrieve information
        assistant = self.openai_client.beta.assistants.create(
            name="RAG Book Content Assistant",
            description="An assistant that answers questions about book content using retrieved information from a vector database",
            model="gpt-4-turbo",  # Using a capable model
            instructions="You are a helpful assistant that answers questions based on retrieved content from book documentation. Always base your answers on the information provided by the retrieval tool. If the retrieved content doesn't answer the question, say so clearly.",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "retrieve_content",
                        "description": "Retrieve relevant content from the book documentation based on the user's query",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The query to search for in the documentation"
                                }
                            },
                            "required": ["query"]
                        }
                    }
                }
            ]
        )

        logger.info(f"Assistant created with ID: {assistant.id}")
        return assistant

    def _retrieve_content(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve content from Qdrant based on the query

        Args:
            query: The query to search for

        Returns:
            List of retrieved chunks with metadata
        """
        try:
            # Use the search_text method from QdrantService
            results = self.qdrant_service.search_text(query, limit=5)

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
            return retrieved_chunks

        except Exception as e:
            logger.error(f"Error retrieving content for query '{query}': {str(e)}")
            return []

    def query(self, question: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Query the agent with a question

        Args:
            question: The question to ask
            session_id: Optional session ID for conversation context

        Returns:
            Dictionary containing the response and metadata
        """
        logger.info(f"Processing query: {question}")

        # Create a thread for the conversation
        thread = self.openai_client.beta.threads.create()

        # Add the user's message to the thread
        self.openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )

        # Run the assistant
        run = self.openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id
        )

        # Wait for the run to complete and handle tool calls
        while run.status in ["queued", "in_progress", "requires_action"]:
            import time
            time.sleep(1)  # Wait a bit before checking again
            run = self.openai_client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            # Handle tool calls if needed
            if run.status == "requires_action":
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []

                for tool_call in tool_calls:
                    if tool_call.function.name == "retrieve_content":
                        # Parse the function arguments
                        args = json.loads(tool_call.function.arguments)
                        query = args.get("query", question)  # Use the question if no specific query provided

                        # Retrieve content using our internal method
                        retrieved_chunks = self._retrieve_content(query)

                        # Format the output for the assistant
                        output = {
                            "retrieved_chunks": retrieved_chunks,
                            "count": len(retrieved_chunks)
                        }

                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(output)
                        })

                # Submit the tool outputs
                self.openai_client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

        # Get the messages from the thread
        messages = self.openai_client.beta.threads.messages.list(
            thread_id=thread.id,
            order="asc"
        )

        # Extract the assistant's response
        assistant_response = ""
        for msg in messages.data:
            if msg.role == "assistant":
                for content_block in msg.content:
                    if content_block.type == "text":
                        assistant_response = content_block.text.value
                        break

        # Get retrieved content to include in response
        retrieved_chunks = self._retrieve_content(question)
        citations = [chunk["source_url"] for chunk in retrieved_chunks if chunk.get("source_url")]

        # Return the response with metadata
        return {
            "response": assistant_response,
            "session_id": session_id or thread.id,  # Use thread ID as session ID if not provided
            "retrieved_chunks": retrieved_chunks,  # Include retrieved chunks for reference
            "citations": citations  # Include citations
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