#!/usr/bin/env python3
"""
Simplified test for Performance Validation Pipeline
"""

import sys
import time
from core.helm.performance_validation_pipeline import (
    create_performance_validation_pipeline,
    create_performance_benchmark,
    BenchmarkType
)

def simple_function():
    """Simple test function"""
    return sum(range(100))

def test_simple():
    print("🔧 Testing Performance Validation Pipeline (Simplified)")
    print("=" * 50)
    
    try:
        # Test 1: Basic Creation
        print("🏗️ Test 1: Basic Creation")
        pipeline = create_performance_validation_pipeline()
        print(f"   Pipeline created: ✅")
        
        # Test 2: Benchmark Creation
        print("\n📊 Test 2: Benchmark Creation")
        benchmark = create_performance_benchmark(
            "test_bench",
            "Test Benchmark",
            simple_function,
            BenchmarkType.LATENCY,
            iterations=3
        )
        print(f"   Benchmark created: ✅")
        
        # Test 3: Registration
        print("\n📝 Test 3: Registration")
        pipeline.register_benchmark(benchmark)
        print(f"   Benchmark registered: ✅")
        print(f"   Registered count: {len(pipeline.benchmarks)}")
        
        # Test 4: Simple Pipeline Run
        print("\n🔄 Test 4: Simple Pipeline Run")
        result = pipeline.run_validation_pipeline()
        print(f"   Pipeline executed: ✅")
        print(f"   Benchmarks run: {result.get('benchmarks_run', 0)}")
        
        print("\n✅ Simplified test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple()
    sys.exit(0 if success else 1)
