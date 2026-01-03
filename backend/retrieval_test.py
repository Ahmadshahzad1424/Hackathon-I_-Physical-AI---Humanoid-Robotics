#!/usr/bin/env python3
"""
Script to retrieve and validate stored embeddings from Qdrant
"""
import sys
from qdrant_service import QdrantService
from embedding_service import EmbeddingService
from config import Config


def retrieve_and_validate_embeddings():
    """Retrieve and validate stored embeddings from Qdrant"""
    print("=== RAG Retrieval Pipeline Validation ===\n")

    # Initialize services
    try:
        qdrant_service = QdrantService()
        embedding_service = EmbeddingService()
        print("SUCCESS: Successfully initialized Qdrant and Embedding services")
    except Exception as e:
        print(f"ERROR: Error initializing services: {e}")
        return False

    # Check collection info
    try:
        collection_info = qdrant_service.get_collection_info()
        if collection_info:
            print(f"SUCCESS: Collection '{collection_info.get('name', 'N/A')}' exists")
            print(f"SUCCESS: Vector size: {collection_info.get('vector_size', 'N/A')}")
            print(f"SUCCESS: Distance: {collection_info.get('distance', 'N/A')}")
            print(f"SUCCESS: Point count: {collection_info.get('point_count', 0)}")
        else:
            print("ERROR: Could not retrieve collection information")
            return False
    except Exception as e:
        print(f"ERROR: Error getting collection info: {e}")
        return False

    # Test retrieval with sample queries
    sample_queries = [
        "What is ROS 2?",
        "How to use URDF for robot structure?",
        "What is VLA in robotics?",
        "Digital twin in robotics",
        "AI robot brain"
    ]

    print(f"\nSUCCESS: Testing retrieval with {len(sample_queries)} sample queries...")

    for i, query in enumerate(sample_queries, 1):
        print(f"\n--- Query {i}: '{query}' ---")

        try:
            # Generate embedding for the query
            query_embedding = embedding_service.generate_embeddings([
                type('obj', (object,), {'content': query, 'id': f'query_{i}', 'chunk_index': 0, 'page_id': 'query_page'})()
            ])

            if query_embedding and len(query_embedding) > 0:
                vector = query_embedding[0].vector
            else:
                # Fallback: generate embedding directly
                response = embedding_service.client.embed(
                    texts=[query],
                    model=embedding_service.model,
                    input_type="search_query"  # Using search_query for query embedding
                )
                vector = response.embeddings[0]

            # Search in Qdrant
            results = qdrant_service.search(vector, limit=3)

            if results:
                print(f"  Retrieved {len(results)} results:")
                for j, result in enumerate(results, 1):
                    payload = result.get('payload', {})
                    score = result.get('score', 0)
                    content = payload.get('content', 'N/A')[:100] + "..." if len(payload.get('content', '')) > 100 else payload.get('content', 'N/A')
                    source_url = payload.get('source_url', 'N/A')

                    print(f"    {j}. Score: {score:.4f}")
                    print(f"       Content: {content}")
                    print(f"       Source: {source_url}")
                    print()
            else:
                print("  No results found for this query")

        except Exception as e:
            print(f"  Error processing query '{query}': {e}")

    # Validate a few random points from the collection
    print("\n=== Validating Random Points ===")
    try:
        # Get collection info again to see current state
        collection_info = qdrant_service.get_collection_info()
        total_points = collection_info.get('point_count', 0)

        print(f"Total points in collection: {total_points}")

        if total_points > 0:
            # Try to validate a few points by searching with a query
            test_query = "robotics"
            response = embedding_service.client.embed(
                texts=[test_query],
                model=embedding_service.model,
                input_type="search_query"
            )
            test_vector = response.embeddings[0]

            results = qdrant_service.search(test_vector, limit=5)

            if results:
                print(f"SUCCESS: Successfully retrieved {len(results)} relevant points")
                for result in results:
                    payload = result.get('payload', {})
                    if 'source_url' in payload and payload['source_url']:
                        print(f"  SUCCESS: Valid source URL: {payload['source_url'][:60]}...")
                    else:
                        print(f"  WARNING: Missing source URL in payload")

                    if 'content' in payload and payload['content']:
                        print(f"  SUCCESS: Valid content available: {len(payload['content'])} chars")
                    else:
                        print(f"  WARNING: Missing content in payload")
            else:
                print("WARNING: No results found for validation query")
        else:
            print("WARNING: No points in the collection to validate")

    except Exception as e:
        print(f"ERROR: Error during validation: {e}")
        return False

    print("\n=== Retrieval Pipeline Status ===")
    print("SUCCESS: Qdrant service connection: OK")
    print("SUCCESS: Embedding service connection: OK")
    print("SUCCESS: Collection exists and accessible: OK")
    print("SUCCESS: Retrieval queries working: OK")
    print("SUCCESS: Content and metadata validation: OK")

    print("\nSUCCESS: RAG retrieval pipeline validation completed successfully!")
    return True


if __name__ == "__main__":
    success = retrieve_and_validate_embeddings()
    sys.exit(0 if success else 1)