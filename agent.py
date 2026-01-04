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
import uuid


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

        # Store active threads for session management
        self.active_threads = {}

        # Store session objects to track conversation history
        self.sessions = {}

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

    def _get_or_create_thread(self, session_id: Optional[str] = None):
        """
        Get an existing thread for the session or create a new one

        Args:
            session_id: Optional session ID to retrieve existing thread

        Returns:
            Thread object
        """
        if session_id and session_id in self.active_threads:
            # Return existing thread
            return self.active_threads[session_id]
        else:
            # Create a new thread
            thread = self.openai_client.beta.threads.create()
            new_session_id = session_id or str(uuid.uuid4())
            self.active_threads[new_session_id] = thread
            return thread

    def query(self, question: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Query the agent with a question

        Args:
            question: The question to ask
            session_id: Optional session ID for conversation context

        Returns:
            Dictionary containing the response and metadata
        """
        logger.info(f"Processing query in session {session_id or 'new'}: {question}")

        # Get or create a thread for the conversation
        thread = self._get_or_create_thread(session_id)
        current_session_id = session_id or list(self.active_threads.keys())[-1]

        # If this is a new session, create an AgentSession object
        if current_session_id not in self.sessions:
            agent_session = AgentSession(
                session_id=current_session_id,
                conversation_context={"messages": [], "thread_id": thread.id},
                metadata={"created_with_assistant_id": self.assistant.id}
            )
            self.sessions[current_session_id] = agent_session

        # Add the user's message to the thread
        self.openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )

        # Add the user's question to the conversation context
        if current_session_id in self.sessions:
            self.sessions[current_session_id].conversation_context["messages"].append({
                "role": "user",
                "content": question,
                "timestamp": str(datetime.now())
            })

        # Run the assistant
        run = self.openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id
        )

        # Wait for the run to complete and handle tool calls
        while run.status in ["queued", "in_progress", "requires_action"]:
            import time
            from datetime import datetime
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

        # Add the assistant's response to the conversation context
        if current_session_id in self.sessions:
            self.sessions[current_session_id].conversation_context["messages"].append({
                "role": "assistant",
                "content": assistant_response,
                "timestamp": str(datetime.now())
            })

        # Get retrieved content to include in response
        retrieved_chunks = self._retrieve_content(question)
        citations = [chunk["source_url"] for chunk in retrieved_chunks if chunk.get("source_url")]

        # Return the response with metadata
        return {
            "response": assistant_response,
            "session_id": current_session_id,
            "thread_id": thread.id,
            "retrieved_chunks": retrieved_chunks,  # Include retrieved chunks for reference
            "citations": citations  # Include citations
        }

    def start_session(self) -> str:
        """
        Start a new conversation session

        Returns:
            Session ID for the new session
        """
        # Create a new thread for the session
        thread = self.openai_client.beta.threads.create()
        session_id = str(uuid.uuid4())

        # Create an AgentSession object to track conversation history
        agent_session = AgentSession(
            session_id=session_id,
            conversation_context={"messages": [], "thread_id": thread.id},
            metadata={"created_with_assistant_id": self.assistant.id}
        )

        # Store the thread and session object
        self.active_threads[session_id] = thread
        self.sessions[session_id] = agent_session

        logger.info(f"Started new session with ID: {session_id}")
        return session_id

    def end_session(self, session_id: str) -> bool:
        """
        End a conversation session and clean up resources

        Args:
            session_id: ID of the session to end

        Returns:
            True if session was ended successfully, False otherwise
        """
        if session_id in self.active_threads:
            # In a real implementation, we might want to archive the thread
            # For now, just remove it from active threads
            del self.active_threads[session_id]
            logger.info(f"Ended session with ID: {session_id}")
            return True
        else:
            logger.warning(f"Attempted to end non-existent session: {session_id}")
            return False


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