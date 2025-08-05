#!/usr/bin/env python3
"""
P.I.T.C.E.S. Performance Optimization Test Suite
Task 307: P.I.T.C.E.S. Performance Optimization and Caching

Comprehensive test suite for P.I.T.C.E.S. performance optimization
including caching, parallel processing, resource management, and
integrated optimization features.
"""

import unittest
import time
import threading
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.pitces.performance import (
    CacheManager, ParallelProcessor, ResourceManager, PerformanceOptimizer,
    ProcessingMode, ResourceType, ResourcePriority
)

class TestCacheManager(unittest.TestCase):
    """Test cases for Cache Manager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.cache_config = {
            "max_memory_mb": 64,
            "default_ttl_seconds": 300,
            "max_entries": 1000,
            "cleanup_interval_seconds": 60,
            "enable_persistence": False
        }
        self.cache_manager = CacheManager(self.cache_config)
    
    def tearDown(self):
        """Clean up after tests"""
        self.cache_manager.shutdown()
    
    def test_cache_put_and_get(self):
        """Test basic cache put and get operations"""
        key = "test_key"
        value = {"data": "test_value", "number": 42}
        category = "test_category"
        
        # Put value in cache
        result = self.cache_manager.put(key, value, category)
        self.assertTrue(result)
        
        # Get value from cache
        cached_value = self.cache_manager.get(key, category)
        self.assertEqual(cached_value, value)
    
    def test_cache_ttl_expiration(self):
        """Test cache TTL expiration"""
        key = "ttl_test"
        value = "expires_soon"
        category = "test"
        ttl = 0.1  # 100ms
        
        # Put with short TTL
        self.cache_manager.put(key, value, category, ttl=ttl)
        
        # Should be available immediately
        cached_value = self.cache_manager.get(key, category)
        self.assertEqual(cached_value, value)
        
        # Wait for expiration
        time.sleep(0.2)
        
        # Should be expired
        cached_value = self.cache_manager.get(key, category)
        self.assertIsNone(cached_value)
    
    def test_cache_invalidation(self):
        """Test cache invalidation"""
        key = "invalidate_test"
        value = "will_be_invalidated"
        category = "test"
        
        # Put and verify
        self.cache_manager.put(key, value, category)
        self.assertEqual(self.cache_manager.get(key, category), value)
        
        # Invalidate and verify
        result = self.cache_manager.invalidate(key, category)
        self.assertTrue(result)
        self.assertIsNone(self.cache_manager.get(key, category))
    
    def test_cache_invalidation_by_tags(self):
        """Test cache invalidation by tags"""
        # Put entries with tags
        self.cache_manager.put("key1", "value1", "test", tags=["tag1", "tag2"])
        self.cache_manager.put("key2", "value2", "test", tags=["tag2", "tag3"])
        self.cache_manager.put("key3", "value3", "test", tags=["tag3"])
        
        # Invalidate by tag
        invalidated = self.cache_manager.invalidate_by_tags(["tag2"])
        self.assertEqual(invalidated, 2)  # key1 and key2 should be invalidated
        
        # Verify invalidation
        self.assertIsNone(self.cache_manager.get("key1", "test"))
        self.assertIsNone(self.cache_manager.get("key2", "test"))
        self.assertIsNotNone(self.cache_manager.get("key3", "test"))
    
    def test_cache_stats(self):
        """Test cache statistics"""
        # Initial stats
        stats = self.cache_manager.get_stats()
        initial_hits = stats["hits"]
        initial_misses = stats["misses"]
        
        # Cache miss
        self.cache_manager.get("nonexistent", "test")
        
        # Cache put and hit
        self.cache_manager.put("stats_test", "value", "test")
        self.cache_manager.get("stats_test", "test")
        
        # Check updated stats
        stats = self.cache_manager.get_stats()
        self.assertEqual(stats["hits"], initial_hits + 1)
        self.assertEqual(stats["misses"], initial_misses + 1)
        self.assertGreater(stats["hit_rate"], 0.0)

class TestParallelProcessor(unittest.TestCase):
    """Test cases for Parallel Processor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor_config = {
            "max_workers": 4,
            "default_timeout": 30,
            "enable_adaptive_scaling": False
        }
        self.processor = ParallelProcessor(self.processor_config)
    
    def tearDown(self):
        """Clean up after tests"""
        self.processor.shutdown()
    
    def test_submit_and_get_result(self):
        """Test task submission and result retrieval"""
        def test_function(x, y):
            return x + y
        
        task_id = "test_task"
        result = self.processor.submit_task(task_id, test_function, 5, 3)
        self.assertEqual(result, task_id)
        
        # Get result
        task_result = self.processor.get_result(task_id, timeout=5)
        self.assertTrue(task_result.success)
        self.assertEqual(task_result.result, 8)
    
    def test_submit_batch_tasks(self):
        """Test batch task submission"""
        def multiply(x, y):
            return x * y
        
        tasks = [
            {"task_id": "batch_1", "function": multiply, "args": (2, 3)},
            {"task_id": "batch_2", "function": multiply, "args": (4, 5)},
            {"task_id": "batch_3", "function": multiply, "args": (6, 7)}
        ]
        
        task_ids = self.processor.submit_batch(tasks)
        self.assertEqual(len(task_ids), 3)
        
        # Get all results
        results = self.processor.get_results(task_ids, timeout=10)
        self.assertEqual(len(results), 3)
        
        # Verify results
        self.assertEqual(results["batch_1"].result, 6)
        self.assertEqual(results["batch_2"].result, 20)
        self.assertEqual(results["batch_3"].result, 42)
    
    def test_task_with_dependencies(self):
        """Test task dependencies"""
        def add_one(x):
            return x + 1
        
        # Submit tasks with dependencies
        self.processor.submit_task("task_1", add_one, 1)
        self.processor.submit_task("task_2", add_one, 2, dependencies=["task_1"])
        
        # Get results
        result_1 = self.processor.get_result("task_1", timeout=5)
        result_2 = self.processor.get_result("task_2", timeout=5)
        
        self.assertTrue(result_1.success)
        self.assertTrue(result_2.success)
        self.assertEqual(result_1.result, 2)
        self.assertEqual(result_2.result, 3)
    
    def test_task_cancellation(self):
        """Test task cancellation"""
        def slow_function():
            time.sleep(1)
            return "completed"
        
        task_id = "cancel_test"
        self.processor.submit_task(task_id, slow_function)
        
        # Cancel task
        cancelled = self.processor.cancel_task(task_id)
        self.assertTrue(cancelled)
        
        # Task should not be in active tasks
        self.assertNotIn(task_id, self.processor.active_tasks)
    
    def test_processor_stats(self):
        """Test processor statistics"""
        def simple_task():
            return "done"
        
        # Submit and complete a task
        self.processor.submit_task("stats_test", simple_task)
        result = self.processor.get_result("stats_test", timeout=5)
        
        # Check stats
        stats = self.processor.get_stats()
        self.assertGreaterEqual(stats["total_tasks"], 1)
        self.assertGreaterEqual(stats["completed_tasks"], 1)
        self.assertGreater(stats["average_processing_time"], 0)

class TestResourceManager(unittest.TestCase):
    """Test cases for Resource Manager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.resource_config = {
            "memory_limit_percent": 80.0,
            "cpu_limit_percent": 80.0,
            "enable_auto_gc": False,
            "monitoring_interval": 1
        }
        self.resource_manager = ResourceManager(self.resource_config)
    
    def tearDown(self):
        """Clean up after tests"""
        self.resource_manager.shutdown()
    
    def test_resource_allocation(self):
        """Test resource allocation and deallocation"""
        component_id = "test_component"
        resource_type = ResourceType.MEMORY
        amount = 100.0  # MB
        
        # Allocate resource
        allocated = self.resource_manager.allocate_resource(
            component_id, resource_type, amount
        )
        self.assertTrue(allocated)
        
        # Check allocation exists
        allocation_key = f"{component_id}:{resource_type.value}"
        self.assertIn(allocation_key, self.resource_manager.allocations)
        
        # Deallocate resource
        deallocated = self.resource_manager.deallocate_resource(
            component_id, resource_type
        )
        self.assertTrue(deallocated)
        self.assertNotIn(allocation_key, self.resource_manager.allocations)
    
    def test_resource_usage_monitoring(self):
        """Test resource usage monitoring"""
        # Get memory usage
        memory_usage = self.resource_manager.get_resource_usage(ResourceType.MEMORY)
        
        self.assertEqual(memory_usage.resource_type, ResourceType.MEMORY)
        self.assertGreaterEqual(memory_usage.current_usage, 0.0)
        self.assertEqual(memory_usage.unit, "%")
        
        # Get CPU usage
        cpu_usage = self.resource_manager.get_resource_usage(ResourceType.CPU)
        
        self.assertEqual(cpu_usage.resource_type, ResourceType.CPU)
        self.assertGreaterEqual(cpu_usage.current_usage, 0.0)
        self.assertEqual(cpu_usage.unit, "%")
    
    def test_memory_optimization(self):
        """Test memory optimization"""
        # Run memory optimization
        result = self.resource_manager.optimize_memory()
        
        self.assertIn("objects_collected", result)
        self.assertIn("memory_freed_mb", result)
        self.assertIn("optimization_time", result)
        self.assertGreaterEqual(result["objects_collected"], 0)
    
    def test_resource_health_check(self):
        """Test resource health checking"""
        health = self.resource_manager.check_resource_health()
        
        self.assertIn("overall_status", health)
        self.assertIn("resource_status", health)
        self.assertIn("warnings", health)
        self.assertIn("critical_issues", health)
        
        # Should have status for memory and CPU
        self.assertIn("memory", health["resource_status"])
        self.assertIn("cpu", health["resource_status"])

class TestPerformanceOptimizer(unittest.TestCase):
    """Test cases for Performance Optimizer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.optimizer_config = {
            "default_profile": "development",
            "enable_auto_optimization": False,
            "monitoring_interval": 1
        }
        self.optimizer = PerformanceOptimizer(self.optimizer_config)
    
    def tearDown(self):
        """Clean up after tests"""
        self.optimizer.shutdown()
    
    def test_profile_switching(self):
        """Test optimization profile switching"""
        # Start with development profile
        self.assertEqual(self.optimizer.current_profile, "development")
        
        # Switch to balanced profile
        result = self.optimizer.set_profile("balanced")
        self.assertTrue(result)
        self.assertEqual(self.optimizer.current_profile, "balanced")
        
        # Try invalid profile
        result = self.optimizer.set_profile("nonexistent")
        self.assertFalse(result)
        self.assertEqual(self.optimizer.current_profile, "balanced")
    
    def test_workload_optimization(self):
        """Test automatic workload optimization"""
        # High complexity workload
        workload = {
            "task_count": 100,
            "complexity_score": 0.9,
            "team_size": 15,
            "parallel_potential": 0.8,
            "memory_intensive": True
        }
        
        profile = self.optimizer.optimize_for_workload(workload)
        self.assertEqual(profile, "high_performance")
        
        # Low complexity workload
        workload = {
            "task_count": 2,
            "complexity_score": 0.2,
            "team_size": 1,
            "parallel_potential": 0.1,
            "memory_intensive": False
        }
        
        profile = self.optimizer.optimize_for_workload(workload)
        self.assertEqual(profile, "resource_conservative")
    
    def test_cache_optimization(self):
        """Test cache optimization"""
        access_pattern = {
            "hit_rate": 0.3,  # Low hit rate
            "avg_access_frequency": 15.0,  # High frequency
            "memory_pressure": False
        }
        
        result = self.optimizer.optimize_cache_for_pattern(access_pattern)
        
        self.assertIn("optimizations_applied", result)
        self.assertIn("current_hit_rate", result)
        self.assertIn("cache_stats", result)
        self.assertGreater(len(result["optimizations_applied"]), 0)
    
    def test_parallel_processing_optimization(self):
        """Test parallel processing optimization"""
        task_characteristics = {
            "cpu_bound": True,
            "io_bound": False,
            "task_count": 10,
            "avg_task_duration": 2.0
        }
        
        result = self.optimizer.optimize_parallel_processing(task_characteristics)
        
        self.assertIn("recommended_mode", result)
        self.assertIn("optimizations_applied", result)
        self.assertIn("processor_stats", result)
        self.assertEqual(result["recommended_mode"], "process")
    
    def test_performance_analysis(self):
        """Test performance analysis"""
        analysis = self.optimizer.run_performance_analysis()
        
        self.assertIn("timestamp", analysis)
        self.assertIn("cache_analysis", analysis)
        self.assertIn("parallel_analysis", analysis)
        self.assertIn("resource_analysis", analysis)
        self.assertIn("recommendations", analysis)
        
        # Check analysis components
        cache_analysis = analysis["cache_analysis"]
        self.assertIn("hit_rate", cache_analysis)
        self.assertIn("performance_rating", cache_analysis)
        
        parallel_analysis = analysis["parallel_analysis"]
        self.assertIn("active_tasks", parallel_analysis)
        self.assertIn("performance_rating", parallel_analysis)
        
        resource_analysis = analysis["resource_analysis"]
        self.assertIn("overall_health", resource_analysis)
        self.assertIn("performance_rating", resource_analysis)
    
    def test_performance_metrics(self):
        """Test performance metrics collection"""
        metrics = self.optimizer.get_performance_metrics()
        
        self.assertIn("optimizer_stats", metrics)
        self.assertIn("current_profile", metrics)
        self.assertIn("cache_metrics", metrics)
        self.assertIn("parallel_metrics", metrics)
        self.assertIn("resource_metrics", metrics)
        
        self.assertEqual(metrics["current_profile"], "development")

def run_performance_demo():
    """Run a demonstration of performance optimization features"""
    print("🚀 P.I.T.C.E.S. Performance Optimization Demo")
    print("=" * 60)
    
    try:
        # Create performance optimizer
        optimizer = PerformanceOptimizer({"default_profile": "balanced"})
        
        print("✅ Performance Optimizer initialized")
        
        # Test workload optimization
        print("\n📊 Testing workload optimization...")
        workload = {
            "task_count": 25,
            "complexity_score": 0.6,
            "team_size": 5,
            "parallel_potential": 0.7,
            "memory_intensive": False
        }
        
        profile = optimizer.optimize_for_workload(workload)
        print(f"   Recommended profile: {profile}")
        
        # Test performance analysis
        print("\n🔍 Running performance analysis...")
        analysis = optimizer.run_performance_analysis()
        
        print(f"   Cache performance: {analysis['cache_analysis']['performance_rating']}/10")
        print(f"   Parallel performance: {analysis['parallel_analysis']['performance_rating']}/10")
        print(f"   Resource health: {analysis['resource_analysis']['overall_health']}")
        
        if analysis["recommendations"]:
            print("   Recommendations:")
            for rec in analysis["recommendations"]:
                print(f"     • {rec}")
        else:
            print("   No recommendations - performance is optimal!")
        
        # Cleanup
        optimizer.shutdown()
        
        print(f"\n✅ Performance optimization demo completed successfully")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == '__main__':
    # Run tests
    print("Running P.I.T.C.E.S. Performance Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "="*60)
    
    # Run demo
    run_performance_demo()
