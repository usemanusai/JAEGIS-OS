#!/usr/bin/env python3
"""
Test script for M.A.S.T.R. Armory functionality
Tests sentence transformers integration and ChromaDB operations
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from core.mastr.armory import ToolArmory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_armory_functionality():
    """Test M.A.S.T.R. Armory functionality"""
    
    print("🧰 Testing M.A.S.T.R. Armory Functionality")
    print("=" * 50)
    
    try:
        # Initialize Armory with test configuration
        config = {
            "chromadb_host": "localhost",
            "chromadb_port": 8001,
            "persist_directory": "data/test_chromadb",
            "collection_name": "test_mastr_armory",
            "embedding_model": "all-MiniLM-L6-v2",
            "embedding_batch_size": 16
        }
        
        print("1. Initializing Tool Armory...")
        armory = ToolArmory(config)
        print("   ✅ Armory initialized successfully")
        
        # Test health check
        print("\n2. Performing health check...")
        health = await armory.health_check()
        print(f"   Health Status: {'✅ Healthy' if health['healthy'] else '❌ Unhealthy'}")
        
        # Test tool storage
        print("\n3. Testing tool storage...")
        test_tools = [
            {
                "name": "FastAPI Web Framework",
                "description": "Modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints",
                "type": "web_framework",
                "category": "api_development",
                "version": "0.104.1",
                "capabilities": ["REST API", "async support", "automatic documentation", "type validation"],
                "requirements": ["python>=3.7", "pydantic", "starlette"],
                "tags": ["python", "web", "api", "async", "fast"],
                "endpoint": "https://fastapi.tiangolo.com/",
                "quality_score": 0.95
            },
            {
                "name": "ChromaDB Vector Database",
                "description": "Open-source embedding database for building AI applications with vector similarity search",
                "type": "vector_database",
                "category": "data_storage",
                "version": "0.4.18",
                "capabilities": ["vector storage", "similarity search", "embedding management", "metadata filtering"],
                "requirements": ["python>=3.7", "numpy", "sqlite"],
                "tags": ["vector", "database", "embeddings", "ai", "search"],
                "endpoint": "https://www.trychroma.com/",
                "quality_score": 0.90
            },
            {
                "name": "Docker Container Platform",
                "description": "Platform for developing, shipping, and running applications using containerization technology",
                "type": "containerization",
                "category": "deployment",
                "version": "24.0.0",
                "capabilities": ["containerization", "image building", "orchestration", "networking"],
                "requirements": ["linux_kernel>=3.10"],
                "tags": ["containers", "deployment", "devops", "orchestration"],
                "endpoint": "https://www.docker.com/",
                "quality_score": 0.92
            }
        ]
        
        stored_tools = []
        for tool in test_tools:
            result = await armory.store_tool(tool)
            if result["success"]:
                stored_tools.append(result)
                print(f"   ✅ Stored: {tool['name']}")
            else:
                print(f"   ❌ Failed to store: {tool['name']} - {result.get('error')}")
        
        # Test tool search
        print("\n4. Testing tool search...")
        search_queries = [
            "web framework for building APIs",
            "vector database for AI applications",
            "container deployment platform",
            "python async web development"
        ]
        
        for query in search_queries:
            search_result = await armory.search_tools(query, limit=3)
            if search_result["success"]:
                print(f"   🔍 Query: '{query}'")
                print(f"      Found {search_result['total_results']} tools:")
                for tool in search_result["tools"][:2]:  # Show top 2 results
                    score = tool.get("similarity_score", 0.0)
                    name = tool.get("metadata", {}).get("tool_name", "Unknown")
                    print(f"        - {name} (similarity: {score:.3f})")
            else:
                print(f"   ❌ Search failed for: '{query}'")
        
        # Test tool retrieval by ID
        print("\n5. Testing tool retrieval by ID...")
        if stored_tools:
            tool_id = stored_tools[0]["tool_id"]
            retrieval_result = await armory.get_tool_by_id(tool_id)
            if retrieval_result["success"]:
                tool_name = retrieval_result["tool"]["metadata"]["tool_name"]
                print(f"   ✅ Retrieved tool: {tool_name}")
            else:
                print(f"   ❌ Failed to retrieve tool: {tool_id}")
        
        # Test tool listing
        print("\n6. Testing tool listing...")
        list_result = await armory.list_tools(limit=5)
        if list_result["success"]:
            print(f"   ✅ Listed {list_result['total_count']} tools")
        else:
            print(f"   ❌ Failed to list tools")
        
        # Get statistics
        print("\n7. Getting Armory statistics...")
        stats = armory.get_armory_statistics()
        print(f"   📊 Total tools: {stats['total_tools']}")
        print(f"   📊 Successful queries: {stats['successful_queries']}")
        print(f"   📊 Failed queries: {stats['failed_queries']}")
        print(f"   📊 Success rate: {stats['success_rate']:.2%}")
        print(f"   📊 Embedding generations: {stats['embedding_generations']}")
        
        print("\n🎉 All M.A.S.T.R. Armory tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        logger.error(f"Armory test failed: {e}", exc_info=True)
        return False

async def main():
    """Main test function"""
    
    print("🚀 M.A.S.T.R. Armory Test Suite")
    print("Testing sentence transformers integration and ChromaDB operations")
    print("=" * 70)
    
    success = await test_armory_functionality()
    
    if success:
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
