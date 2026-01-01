#!/usr/bin/env python3
"""
Script to check the number of points in the Qdrant collection
"""
from qdrant_service import QdrantService

def check_collection_points():
    """Check the number of points in the Qdrant collection"""
    qdrant_service = QdrantService()

    collection_info = qdrant_service.get_collection_info()

    if collection_info:
        print(f"Collection Name: {collection_info.get('name', 'N/A')}")
        print(f"Vector Size: {collection_info.get('vector_size', 'N/A')}")
        print(f"Distance: {collection_info.get('distance', 'N/A')}")
        print(f"Point Count: {collection_info.get('point_count', 0)}")
        print(f"Points (Approx): {collection_info.get('point_count', 0)}")
    else:
        print("Could not retrieve collection information")

if __name__ == "__main__":
    check_collection_points()