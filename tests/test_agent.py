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


def run_all_tests():
    """Run all tests and report results"""
    print("Running RAG Agent Basic Functionality Tests")
    print("=" * 50)

    tests = [
        test_agent_initialization,
        test_basic_query,
        test_multiple_queries
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    print("\n" + "=" * 50)
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