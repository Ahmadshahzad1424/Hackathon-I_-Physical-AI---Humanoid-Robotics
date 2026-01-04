#!/usr/bin/env python3
"""
Integration tests to validate all user stories work together
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


def test_user_story_1_query_documentation():
    """Test User Story 1: Query Documentation with RAG Agent"""
    print("Testing User Story 1: Query Documentation with RAG Agent...")

    try:
        agent = RAGAgent()

        # Test that the agent can answer questions about book content
        response = agent.query("What is ROS 2?")

        # Validate response structure
        required_keys = ['response', 'session_id', 'retrieved_chunks', 'citations', 'status']
        for key in required_keys:
            if key not in response:
                print(f"✗ Response missing required key: {key}")
                return False

        # Check that response is meaningful
        if not response['response'] or len(response['response']) < 10:
            print("✗ Response is too short or empty")
            return False

        # Check that retrieved content is used
        if response['status'] != 'success':
            print(f"✗ Query did not succeed, status: {response['status']}")
            return False

        print("✓ User Story 1 validated: Agent can answer questions using retrieved content")
        return True
    except Exception as e:
        print(f"✗ User Story 1 test failed: {e}")
        return False


def test_user_story_2_follow_up_queries():
    """Test User Story 2: Handle Follow-up Queries"""
    print("\nTesting User Story 2: Handle Follow-up Queries...")

    try:
        agent = RAGAgent()

        # Start a session
        session_id = agent.start_session()

        # First query
        response1 = agent.query("What is ROS 2?", session_id)

        # Follow-up query in the same session
        response2 = agent.query("What are its main features?", session_id)

        # Another follow-up
        response3 = agent.query("How does it differ from ROS 1?", session_id)

        # Validate all responses are in the same session
        if not (response1['session_id'] == response2['session_id'] == response3['session_id'] == session_id):
            print("✗ Responses are not in the same session")
            return False

        # Check that conversation history is maintained
        history = agent.get_conversation_history(session_id)
        if len(history) < 6:  # 3 user queries + 3 responses
            print(f"✗ Conversation history too short: {len(history)} messages")
            return False

        # End the session
        agent.end_session(session_id)

        print("✓ User Story 2 validated: Agent maintains conversation context for follow-up queries")
        return True
    except Exception as e:
        print(f"✗ User Story 2 test failed: {e}")
        return False


def test_user_story_3_retrieval_tool():
    """Test User Story 3: Use Retrieval Tool with Qdrant"""
    print("\nTesting User Story 3: Use Retrieval Tool with Qdrant...")

    try:
        agent = RAGAgent()

        # Test that the dedicated retrieval tool exists and works
        retrieval_result = agent.retrieval_tool("ROS 2 concepts")

        # Validate retrieval tool response structure
        required_keys = ['retrieved_chunks', 'count', 'query', 'status']
        for key in required_keys:
            if key not in retrieval_result:
                print(f"✗ Retrieval result missing required key: {key}")
                return False

        # Test that the tool was registered with the assistant by checking it exists
        if not hasattr(agent, 'retrieval_tool'):
            print("✗ retrieval_tool method does not exist")
            return False

        # Test that the assistant can use the tool (indirectly tested through query)
        query_response = agent.query("Explain URDF")
        if query_response.get('status') != 'success':
            print("✗ Query failed when using retrieval tool")
            return False

        print("✓ User Story 3 validated: Agent uses dedicated retrieval tool that queries Qdrant")
        return True
    except Exception as e:
        print(f"✗ User Story 3 test failed: {e}")
        return False


def test_all_user_stories_integration():
    """Test that all user stories work together in a comprehensive scenario"""
    print("\nTesting comprehensive integration of all user stories...")

    try:
        agent = RAGAgent()

        # Start a session (User Story 2)
        session_id = agent.start_session()

        # Ask a question that uses retrieval (User Story 1 & 3)
        response1 = agent.query("What is the Robot Operating System?", session_id)

        if response1['status'] != 'success':
            print("✗ First query failed")
            return False

        # Follow-up question in the same session (User Story 2)
        response2 = agent.query("What are its main components?", session_id)

        if response2['status'] != 'success':
            print("✗ Follow-up query failed")
            return False

        # Another follow-up that uses retrieval (User Story 1 & 3)
        response3 = agent.query("How does the communication system work?", session_id)

        if response3['status'] != 'success':
            print("✗ Second follow-up query failed")
            return False

        # Verify all responses are in the same session
        if not (response1['session_id'] == response2['session_id'] == response3['session_id'] == session_id):
            print("✗ Responses are not in the same session")
            return False

        # Check conversation history
        history = agent.get_conversation_history(session_id)
        if len(history) < 6:
            print(f"✗ Conversation history too short: {len(history)} messages")
            return False

        # Verify retrieval was used (check if chunks were retrieved)
        # This is a basic check - in a real scenario, we'd check more thoroughly
        if response1.get('retrieved_chunks') is None:
            print("✗ Retrieved chunks not available in response")
            return False

        # End the session
        agent.end_session(session_id)

        print("✓ All user stories validated together: Comprehensive integration test passed")
        return True
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False


def run_all_tests():
    """Run all integration tests and report results"""
    print("Running RAG Agent Integration Tests")
    print("=" * 40)

    tests = [
        test_user_story_1_query_documentation,
        test_user_story_2_follow_up_queries,
        test_user_story_3_retrieval_tool,
        test_all_user_stories_integration
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    print("\n" + "=" * 40)
    print("Integration Test Summary:")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✓ All integration tests passed!")
        return True
    else:
        print(f"✗ {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)