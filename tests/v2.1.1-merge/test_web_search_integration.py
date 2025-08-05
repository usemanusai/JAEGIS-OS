#!/usr/bin/env python3
"""
Test script for Task 1.1.2: Multi-Source Web Search Integration
Tests Tavily, Serper, and arXiv integration with rate limiting and deduplication
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.utils.web_search import create_web_search_manager, SearchConfig
from core.helm.curator import BenchmarkCurator

async def test_web_search_manager():
    """Test the WebSearchManager with different configurations"""
    
    print("🧪 Testing Multi-Source Web Search Integration")
    print("=" * 60)
    
    # Test 1: Basic search without API keys (arXiv only)
    print("\n📋 Test 1: Basic search (arXiv only)")
    try:
        manager = create_web_search_manager()
        results = await manager.search("machine learning benchmark", max_results=3)
        
        print(f"✅ Found {len(results)} results")
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result.title[:60]}... (source: {result.source})")
            
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
    
    # Test 2: Search with API keys if available
    print("\n📋 Test 2: Multi-source search (if API keys available)")
    try:
        tavily_key = os.getenv("TAVILY_API_KEY")
        serper_key = os.getenv("SERPER_API_KEY")
        
        if tavily_key or serper_key:
            manager = create_web_search_manager(
                tavily_api_key=tavily_key,
                serper_api_key=serper_key
            )
            
            results = await manager.search("NLP evaluation dataset", max_results=5)
            
            print(f"✅ Found {len(results)} results from multiple sources")
            sources = set(result.source for result in results)
            print(f"   Sources used: {', '.join(sources)}")
            
            for i, result in enumerate(results, 1):
                print(f"   {i}. {result.title[:50]}... (source: {result.source}, score: {result.relevance_score:.2f})")
        else:
            print("⚠️  No API keys found in environment, skipping multi-source test")
            
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
    
    # Test 3: Benchmark-specific search
    print("\n📋 Test 3: Benchmark discovery search")
    try:
        manager = create_web_search_manager()
        benchmark_results = await manager.search_benchmarks(
            ["GLUE benchmark", "SuperGLUE"], 
            max_results_per_term=2
        )
        
        print(f"✅ Benchmark search completed")
        for term, results in benchmark_results.items():
            print(f"   {term}: {len(results)} results")
            
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")

async def test_helm_curator_integration():
    """Test the H.E.L.M. Curator with real web search"""
    
    print("\n🎯 Testing H.E.L.M. Curator Integration")
    print("=" * 60)
    
    try:
        # Initialize curator
        curator = BenchmarkCurator()
        
        # Test discovery with limited search terms
        search_terms = ["BERT evaluation", "language model benchmark"]
        
        print(f"🔍 Starting benchmark discovery with terms: {search_terms}")
        discovery_results = await curator.discover_benchmarks(search_terms)
        
        print(f"✅ Discovery completed!")
        print(f"   Total found: {discovery_results['total_found']}")
        print(f"   Curated: {discovery_results['curated_count']}")
        
        # Show results by source
        for source, source_results in discovery_results["sources"].items():
            if "error" in source_results:
                print(f"   {source}: Error - {source_results['error']}")
            else:
                print(f"   {source}: {source_results['found_count']} found, {source_results['curated_count']} curated")
        
    except Exception as e:
        print(f"❌ H.E.L.M. Curator test failed: {e}")

async def test_rate_limiting():
    """Test rate limiting functionality"""
    
    print("\n⏱️  Testing Rate Limiting")
    print("=" * 60)
    
    try:
        from core.utils.web_search import RateLimiter
        
        # Create a rate limiter that allows 2 calls per minute
        limiter = RateLimiter(calls_per_minute=2)
        
        print("🔄 Testing rate limiter (2 calls per minute)...")
        
        start_time = asyncio.get_event_loop().time()
        
        # Make 3 calls - the third should be delayed
        for i in range(3):
            print(f"   Call {i+1}...")
            await limiter.wait_if_needed()
            current_time = asyncio.get_event_loop().time()
            elapsed = current_time - start_time
            print(f"   Call {i+1} completed at {elapsed:.2f}s")
        
        print("✅ Rate limiting test completed")
        
    except Exception as e:
        print(f"❌ Rate limiting test failed: {e}")

async def test_deduplication():
    """Test search result deduplication"""
    
    print("\n🔄 Testing Result Deduplication")
    print("=" * 60)
    
    try:
        from core.utils.web_search import SearchResult, SearchResultDeduplicator
        
        # Create duplicate results
        results = [
            SearchResult(
                title="BERT: Pre-training of Deep Bidirectional Transformers",
                url="https://arxiv.org/abs/1810.04805",
                snippet="We introduce BERT, a new language representation model...",
                source="arxiv",
                timestamp="2024-01-01T00:00:00"
            ),
            SearchResult(
                title="BERT: Pre-training of Deep Bidirectional Transformers",
                url="https://arxiv.org/abs/1810.04805",
                snippet="We introduce BERT, a new language representation model...",
                source="tavily",
                timestamp="2024-01-01T00:01:00"
            ),
            SearchResult(
                title="Different Paper",
                url="https://example.com/different",
                snippet="This is a different paper...",
                source="serper",
                timestamp="2024-01-01T00:02:00"
            )
        ]
        
        deduplicator = SearchResultDeduplicator()
        unique_results = deduplicator.deduplicate(results)
        
        print(f"✅ Deduplication test: {len(results)} -> {len(unique_results)} results")
        print(f"   Original: {len(results)} results")
        print(f"   After deduplication: {len(unique_results)} results")
        
    except Exception as e:
        print(f"❌ Deduplication test failed: {e}")

async def main():
    """Run all tests"""
    
    print("🚀 JAEGIS Multi-Source Web Search Integration Tests")
    print("Task 1.1.2: Multi-Source Web Search Integration")
    print("=" * 80)
    
    # Check for API keys
    tavily_key = os.getenv("TAVILY_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")
    
    print(f"🔑 API Key Status:")
    print(f"   Tavily API Key: {'✅ Available' if tavily_key else '❌ Not set'}")
    print(f"   Serper API Key: {'✅ Available' if serper_key else '❌ Not set'}")
    print(f"   arXiv: ✅ Always available (direct API)")
    
    # Run tests
    await test_rate_limiting()
    await test_deduplication()
    await test_web_search_manager()
    await test_helm_curator_integration()
    
    print("\n🎉 All tests completed!")
    print("\n💡 To test with API keys:")
    print("   export TAVILY_API_KEY='your_key_here'")
    print("   export SERPER_API_KEY='your_key_here'")
    print("   python tests/test_web_search_integration.py")

if __name__ == "__main__":
    asyncio.run(main())
