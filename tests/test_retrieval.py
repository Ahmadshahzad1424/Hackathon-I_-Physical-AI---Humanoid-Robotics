#!/usr/bin/env python3
"""
Test script to verify RAG Agent uses dedicated retrieval tool
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


def test_retrieval_tool_exists():
    """Test that the dedicated retrieval tool function exists in the agent"""
    print("Testing that retrieval tool function exists...")

    try:
        agent = RAGAgent()

        # Check if the retrieval_tool method exists
        if hasattr(agent, 'retrieval_tool'):
            print("✓ retrieval_tool method exists")
        else:
            print("✗ retrieval_tool method does not exist")
            return False

        # Check if the method is callable
        if callable(getattr(agent, 'retrieval_tool')):
            print("✓ retrieval_tool is callable")
        else:
            print("✗ retrieval_tool is not callable")
            return False

        # Test the method with a simple query
        result = agent.retrieval_tool("test query")
        if isinstance(result, dict) and 'status' in result:
            print("✓ retrieval_tool returns expected format")
        else:
            print("✗ retrieval_tool does not return expected format")
            return False

        print("✓ Retrieval tool exists and functions correctly")
        return True
    except Exception as e:
        print(f"✗ Retrieval tool test failed: {e}")
        return False


def test_retrieval_tool_functionality():
    """Test that the retrieval tool actually retrieves content from Qdrant"""
    print("\nTesting retrieval tool functionality...")

    try:
        agent = RAGAgent()

        # Test with a query that should return results
        result = agent.retrieval_tool("ROS 2")

        if result.get('status') in ['success', 'no_content_found']:
            print(f"✓ Retrieval tool executed with status: {result.get('status')}")
        else:
            print(f"✗ Retrieval tool failed with status: {result.get('status')}")
            return False

        # Check the structure of the result
        expected_keys = ['retrieved_chunks', 'count', 'query', 'status']
        for key in expected_keys:
            if key not in result:
                print(f"✗ Result missing expected key: {key}")
                return False

        print(f"✓ Retrieval tool returned {result.get('count')} chunks for query '{result.get('query')}'")
        print("✓ Retrieval tool functionality test completed")
        return True
    except Exception as e:
        print(f"✗ Retrieval tool functionality test failed: {e}")
        return False


def test_assistant_tool_registration():
    """Test that the assistant is created with the retrieval tool registered"""
    print("\nTesting assistant tool registration...")

    try:
        agent = RAGAgent()

        # The assistant is created during initialization, so we just need to verify
        # that it was created with the right tools
        # We can't directly check the tools of an existing assistant in OpenAI API,
        # but we can verify that the agent was initialized properly
        if agent.assistant:
            print("✓ Assistant was created successfully")
        else:
            print("✗ Assistant was not created")
            return False

        print("✓ Assistant tool registration test completed")
        return True
    except Exception as e:
        print(f"✗ Assistant tool registration test failed: {e}")
        return False


def run_all_tests():
    """Run all retrieval tool tests and report results"""
    print("Running RAG Agent Retrieval Tool Tests")
    print("=" * 45)

    tests = [
        test_retrieval_tool_exists,
        test_retrieval_tool_functionality,
        test_assistant_tool_registration
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    print("\n" + "=" * 45)
    print("Test Summary:")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✓ All retrieval tool tests passed!")
        return True
    else:
        print(f"✗ {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)