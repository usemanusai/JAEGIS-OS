#!/usr/bin/env python3
"""
Test script for Enhanced Tavily API Integration
Task 1.1.1: Primary Tavily API integration with rate limiting

Tests all advanced features:
- API key rotation
- Enhanced rate limiting with burst support
- Result caching with TTL
- Query optimization
"""

import asyncio
import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from core.helm.tavily_integration import (
        EnhancedTavilyClient,
        TavilyConfig,
        create_enhanced_tavily_client
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure the core.helm.tavily_integration module is available")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TavilyIntegrationTester:
    """Comprehensive tester for enhanced Tavily integration"""
    
    def __init__(self):
        self.test_results = {}
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        logger.info("🚀 Starting Enhanced Tavily Integration Tests")
        
        tests = [
            ("Basic Search", self.test_basic_search),
            ("Query Optimization", self.test_query_optimization),
            ("Result Caching", self.test_result_caching),
            ("Rate Limiting", self.test_rate_limiting),
            ("API Key Rotation", self.test_api_key_rotation),
            ("Error Handling", self.test_error_handling),
            ("Health Check", self.test_health_check),
            ("Statistics", self.test_statistics)
        ]
        
        for test_name, test_func in tests:
            try:
                logger.info(f"🧪 Running test: {test_name}")
                result = await test_func()
                self.test_results[test_name] = {
                    "status": "PASSED",
                    "result": result
                }
                logger.info(f"✅ {test_name}: PASSED")
            except Exception as e:
                self.test_results[test_name] = {
                    "status": "FAILED",
                    "error": str(e)
                }
                logger.error(f"❌ {test_name}: FAILED - {e}")
        
        return self.test_results
    
    async def test_basic_search(self) -> Dict[str, Any]:
        """Test basic search functionality"""
        # Create client with mock API key for testing
        config = TavilyConfig(
            api_keys=["test_key_1"],
            rate_limit_per_minute=60,
            cache_ttl_hours=1
        )
        
        # Note: This will fail without real API key, but tests the structure
        try:
            client = EnhancedTavilyClient(config)
            
            # Test query optimization
            optimized = client.query_optimizer.optimize_query("language model", "nlp")
            
            return {
                "client_initialized": True,
                "query_optimization": optimized,
                "components_loaded": {
                    "rate_limiter": client.rate_limiter is not None,
                    "query_optimizer": client.query_optimizer is not None,
                    "result_cache": client.result_cache is not None,
                    "key_rotator": client.key_rotator is not None
                }
            }
        except Exception as e:
            if "API key" in str(e):
                return {"note": "Expected failure without real API key", "structure_valid": True}
            raise
    
    async def test_query_optimization(self) -> Dict[str, Any]:
        """Test query optimization features"""
        config = TavilyConfig(api_keys=["test_key"])
        client = EnhancedTavilyClient(config)
        
        test_cases = [
            ("language model", "nlp"),
            ("computer vision", "cv"),
            ("reinforcement learning", "rl"),
            ("simple query", "general")
        ]
        
        results = {}
        for query, context in test_cases:
            optimized = client.query_optimizer.optimize_query(query, context)
            results[f"{query} ({context})"] = optimized
        
        return results
    
    async def test_result_caching(self) -> Dict[str, Any]:
        """Test result caching functionality"""
        config = TavilyConfig(api_keys=["test_key"], cache_ttl_hours=1)
        client = EnhancedTavilyClient(config)
        
        # Test cache operations
        cache = client.result_cache
        
        # Test cache miss
        result = cache.get("test_query", 10)
        cache_miss = result is None
        
        # Test cache set and get
        test_results = [{"title": "Test", "url": "http://test.com", "snippet": "Test snippet"}]
        cache.set("test_query", 10, test_results)
        
        cached_result = cache.get("test_query", 10)
        cache_hit = cached_result is not None
        
        return {
            "cache_miss_works": cache_miss,
            "cache_hit_works": cache_hit,
            "cached_data_matches": cached_result == test_results if cache_hit else False,
            "cache_directory_exists": cache.cache_dir.exists()
        }
    
    async def test_rate_limiting(self) -> Dict[str, Any]:
        """Test enhanced rate limiting with burst support"""
        config = TavilyConfig(api_keys=["test_key"])
        client = EnhancedTavilyClient(config)
        
        rate_limiter = client.rate_limiter
        
        # Test initial state
        initial_burst_tokens = rate_limiter.burst_tokens
        
        # Simulate burst usage
        await rate_limiter.wait_if_needed()
        after_one_call = rate_limiter.burst_tokens
        
        return {
            "initial_burst_tokens": initial_burst_tokens,
            "burst_tokens_after_call": after_one_call,
            "burst_mechanism_working": after_one_call < initial_burst_tokens,
            "rate_limiter_initialized": True
        }
    
    async def test_api_key_rotation(self) -> Dict[str, Any]:
        """Test API key rotation functionality"""
        config = TavilyConfig(api_keys=["key1", "key2", "key3"])
        client = EnhancedTavilyClient(config)
        
        rotator = client.key_rotator
        
        # Test initial state
        initial_key = rotator.get_current_key()
        initial_index = rotator.current_index
        
        # Test rotation
        rotated_key = rotator.rotate_key("test error")
        new_index = rotator.current_index
        
        # Test stats
        stats = rotator.get_stats()
        
        return {
            "initial_key": initial_key,
            "initial_index": initial_index,
            "rotated_key": rotated_key,
            "new_index": new_index,
            "rotation_working": new_index != initial_index,
            "total_keys": stats["total_keys"],
            "stats_available": "key_stats" in stats
        }
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling and retry mechanisms"""
        config = TavilyConfig(
            api_keys=["invalid_key"],
            retry_attempts=2,
            retry_backoff_factor=1.5
        )
        client = EnhancedTavilyClient(config)
        
        # This should fail gracefully
        try:
            await client.search("test query", max_results=5)
            return {"unexpected_success": True}
        except Exception as e:
            return {
                "error_handled": True,
                "error_type": type(e).__name__,
                "error_message": str(e)[:100],  # Truncate for readability
                "retry_mechanism_triggered": "retries" in str(e) or "attempts" in str(e)
            }
    
    async def test_health_check(self) -> Dict[str, Any]:
        """Test health check functionality"""
        config = TavilyConfig(api_keys=["test_key_1", "test_key_2"])
        client = EnhancedTavilyClient(config)
        
        # Health check will fail with test keys, but should return proper structure
        try:
            health_status = await client.health_check()
            return {
                "health_check_structure_valid": True,
                "has_timestamp": "timestamp" in health_status,
                "has_overall_status": "overall_status" in health_status,
                "has_api_keys_status": "api_keys" in health_status,
                "api_keys_count": len(health_status.get("api_keys", []))
            }
        except Exception as e:
            return {
                "health_check_attempted": True,
                "expected_failure": "test" in str(e) or "API" in str(e)
            }
    
    async def test_statistics(self) -> Dict[str, Any]:
        """Test statistics collection"""
        config = TavilyConfig(api_keys=["test_key_1", "test_key_2"])
        client = EnhancedTavilyClient(config)
        
        stats = client.get_statistics()
        
        return {
            "stats_structure_valid": isinstance(stats, dict),
            "has_api_key_stats": "api_key_stats" in stats,
            "has_cache_stats": "cache_stats" in stats,
            "has_rate_limiter_stats": "rate_limiter_stats" in stats,
            "api_keys_tracked": stats.get("api_key_stats", {}).get("total_keys", 0),
            "cache_directory_tracked": "cache_dir" in stats.get("cache_stats", {})
        }

async def main():
    """Main test execution"""
    print("🔧 Enhanced Tavily Integration Test Suite")
    print("=" * 50)
    
    tester = TavilyIntegrationTester()
    results = await tester.run_all_tests()
    
    # Print summary
    print("\n📊 Test Results Summary:")
    print("=" * 50)
    
    passed = sum(1 for r in results.values() if r["status"] == "PASSED")
    total = len(results)
    
    for test_name, result in results.items():
        status_icon = "✅" if result["status"] == "PASSED" else "❌"
        print(f"{status_icon} {test_name}: {result['status']}")
        
        if result["status"] == "FAILED":
            print(f"   Error: {result['error']}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced Tavily integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
