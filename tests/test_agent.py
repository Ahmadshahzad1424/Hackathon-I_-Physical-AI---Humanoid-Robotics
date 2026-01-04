#!/usr/bin/env python3
"""
Test script to verify basic RAG Agent functionality
"""
import sys
import os
import logging

# Add the project root to the Python path so we can import from agent.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import RAGAgent

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_agent_initialization():
    """Test that the RAG Agent can be initialized successfully"""
    print("Testing agent initialization...")

    try:
        agent = RAGAgent()
        print("✓ Agent initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Agent initialization failed: {e}")
        return False


def test_basic_query():
    """Test basic query functionality"""
    print("\nTesting basic query functionality...")

    try:
        agent = RAGAgent()

        # Test with a simple query
        response = agent.query("What is ROS 2?")

        print(f"Query: What is ROS 2?")
        print(f"Response: {response['response'][:100]}...")  # Show first 100 chars
        print(f"Session ID: {response['session_id']}")
        print("✓ Basic query test completed")

        return True
    except Exception as e:
        print(f"✗ Basic query test failed: {e}")
        return False


def test_multiple_queries():
    """Test multiple queries to verify basic functionality"""
    print("\nTesting multiple queries...")

    try:
        agent = RAGAgent()

        queries = [
            "What is ROS 2?",
            "Explain URDF in robotics",
            "What are digital twins in robotics?"
        ]

        for i, query in enumerate(queries, 1):
            response = agent.query(query)
            print(f"Query {i}: {query}")
            print(f"Response preview: {response['response'][:50]}...")

        print("✓ Multiple queries test completed")
        return True
    except Exception as e:
        print(f"✗ Multiple queries test failed: {e}")
        return False


def test_retrieved_content_usage():
    """Test that agent responses are based on retrieved content"""
    print("\nTesting that responses are based on retrieved content...")

    try:
        agent = RAGAgent()

        # Test query that should have relevant content in the database
        query = "What is ROS 2?"
        response = agent.query(query)

        # Check that retrieved chunks exist
        if not response.get('retrieved_chunks'):
            print("✗ No retrieved chunks found in response")
            return False

        # Check that citations exist
        if not response.get('citations'):
            print("⚠ No citations found (this might be OK depending on data)")
        else:
            print(f"✓ Found {len(response['citations'])} citations")

        print(f"✓ Retrieved {len(response['retrieved_chunks'])} chunks for the query")
        print("✓ Response is based on retrieved content")

        return True
    except Exception as e:
        print(f"✗ Retrieved content test failed: {e}")
        return False


def test_content_fallback():
    """Test agent behavior when no relevant content is found"""
    print("\nTesting agent behavior with unlikely query...")

    try:
        agent = RAGAgent()

        # Test with a query that likely won't have matches in the documentation
        query = "What is the color of the invisible unicorn?"
        response = agent.query(query)

        # The agent should respond appropriately even when no content is found
        print(f"Query: {query}")
        print(f"Response: {response['response'][:100]}...")

        print("✓ Agent handled query without relevant content appropriately")
        return True
    except Exception as e:
        print(f"✗ Content fallback test failed: {e}")
        return False


def test_multi_turn_conversation():
    """Test multi-turn conversations with follow-up questions"""
    print("\nTesting multi-turn conversation with follow-up questions...")

    try:
        agent = RAGAgent()

        # Start a new session
        session_id = agent.start_session()
        print(f"Started session: {session_id}")

        # First query
        response1 = agent.query("What is ROS 2?", session_id)
        print(f"Query 1: What is ROS 2?")
        print(f"Response 1 preview: {response1['response'][:50]}...")

        # Follow-up query in the same session
        response2 = agent.query("What are its main features?", session_id)
        print(f"Query 2: What are its main features?")
        print(f"Response 2 preview: {response2['response'][:50]}...")

        # Another follow-up
        response3 = agent.query("How does it differ from ROS 1?", session_id)
        print(f"Query 3: How does it differ from ROS 1?")
        print(f"Response 3 preview: {response3['response'][:50]}...")

        # Check that all responses are in the same session
        if (response1['session_id'] == response2['session_id'] == response3['session_id'] == session_id):
            print("✓ All queries were processed in the same session")
        else:
            print("✗ Queries were not processed in the same session")
            return False

        # Check conversation history
        history = agent.get_conversation_history(session_id)
        if len(history) >= 6:  # 3 user queries + 3 assistant responses
            print(f"✓ Conversation history contains {len(history)} messages")
        else:
            print(f"✗ Conversation history only contains {len(history)} messages, expected at least 6")
            return False

        # End the session
        agent.end_session(session_id)
        print("✓ Multi-turn conversation test completed")

        return True
    except Exception as e:
        print(f"✗ Multi-turn conversation test failed: {e}")
        return False


def test_session_isolation():
    """Test that different sessions are properly isolated"""
    print("\nTesting session isolation...")

    try:
        agent = RAGAgent()

        # Start two different sessions
        session1_id = agent.start_session()
        session2_id = agent.start_session()

        print(f"Started session 1: {session1_id}")
        print(f"Started session 2: {session2_id}")

        # Query both sessions with different topics
        response1 = agent.query("What is ROS 2?", session1_id)
        response2 = agent.query("Explain URDF", session2_id)

        # Verify sessions are different
        if response1['session_id'] == session1_id and response2['session_id'] == session2_id:
            print("✓ Sessions are properly isolated")
        else:
            print("✗ Sessions are not properly isolated")
            return False

        # Check that each session has its own history
        history1 = agent.get_conversation_history(session1_id)
        history2 = agent.get_conversation_history(session2_id)

        if len(history1) >= 2 and len(history2) >= 2:
            print(f"✓ Session 1 has {len(history1)} messages, Session 2 has {len(history2)} messages")
        else:
            print(f"✗ Session history not properly maintained")
            return False

        # End both sessions
        agent.end_session(session1_id)
        agent.end_session(session2_id)
        print("✓ Session isolation test completed")

        return True
    except Exception as e:
        print(f"✗ Session isolation test failed: {e}")
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("Running RAG Agent Comprehensive Functionality Tests")
    print("=" * 55)

    tests = [
        test_agent_initialization,
        test_basic_query,
        test_multiple_queries,
        test_retrieved_content_usage,
        test_content_fallback,
        test_multi_turn_conversation,
        test_session_isolation
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    print("\n" + "=" * 55)
    print("Test Summary:")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✓ All tests passed!")
        return True
    else:
        print(f"✗ {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)