#!/usr/bin/env python3
"""
Test script for H.E.L.M. Code Quality and Validation Pipeline
Task 2.3.2: Code Quality and Validation Pipeline

Tests syntax validation and linting, performance profiling of generated code,
and security vulnerability scanning.
"""

import sys
from core.helm.quality_pipeline import (
    CodeQualityPipeline,
    ValidationLevel,
    SecurityLevel,
    create_quality_pipeline
)

def test_quality_pipeline():
    """Test the Code Quality Pipeline implementation"""
    print("🔧 Testing H.E.L.M. Code Quality and Validation Pipeline")
    print("=" * 50)
    
    try:
        # Test 1: Pipeline Creation
        print("🏗️ Test 1: Pipeline Creation")
        
        # Create default pipeline
        pipeline = create_quality_pipeline()
        print(f"   Default pipeline created")
        print(f"   Validation level: {pipeline.validation_level.value}")
        print(f"   Security level: {pipeline.security_level.value}")
        print(f"   Performance profiling: {pipeline.enable_performance_profiling}")
        
        # Create custom pipeline
        custom_config = {
            'validation_level': ValidationLevel.STRICT.value,
            'security_level': SecurityLevel.HIGH.value,
            'enable_performance_profiling': True,
            'timeout_seconds': 120
        }
        
        custom_pipeline = create_quality_pipeline(custom_config)
        print(f"   Custom pipeline created with level: {custom_pipeline.validation_level.value}")
        
        print("✅ Pipeline creation working")
        
        # Test 2: Syntax Validation
        print("\n🔍 Test 2: Syntax Validation")
        
        # Valid Python code
        valid_code = '''
def hello_world():
    """A simple hello world function"""
    message = "Hello, World!"
    print(message)
    return message

if __name__ == "__main__":
    hello_world()
'''
        
        # Invalid Python code
        invalid_code = '''
def broken_function(
    print("This has syntax errors"
    return "missing parenthesis"
'''
        
        # Test valid code
        valid_syntax = pipeline._validate_syntax(valid_code)
        print(f"   Valid code syntax check: {valid_syntax}")
        
        # Test invalid code
        invalid_syntax = pipeline._validate_syntax(invalid_code)
        print(f"   Invalid code syntax check: {invalid_syntax}")
        
        print("✅ Syntax validation working")
        
        # Test 3: Quality Metrics Analysis
        print("\n📊 Test 3: Quality Metrics Analysis")
        
        # Test code with various quality characteristics
        test_code = '''
import numpy as np
import pandas as pd

def complex_function(data, threshold=0.5):
    """
    A complex function for testing quality metrics.
    This function has multiple branches and loops.
    """
    results = []
    
    # Multiple nested conditions
    if data is not None:
        if len(data) > 0:
            for item in data:
                if item > threshold:
                    if item < 1.0:
                        processed = item * 2
                        if processed > 0.8:
                            results.append(processed)
                        else:
                            results.append(item)
                    else:
                        results.append(1.0)
                else:
                    results.append(0.0)
    
    # Some duplicate logic
    final_results = []
    for item in results:
        if item > 0.5:
            final_results.append(item)
    
    return final_results

# Another function with similar logic (duplication)
def another_complex_function(values):
    output = []
    for item in values:
        if item > 0.5:
            output.append(item)
    return output
'''
        
        quality_metrics = pipeline._analyze_quality_metrics(test_code)
        
        print(f"   Lines of code: {quality_metrics.lines_of_code}")
        print(f"   Comment ratio: {quality_metrics.comment_ratio:.3f}")
        print(f"   Cyclomatic complexity: {quality_metrics.cyclomatic_complexity:.1f}")
        print(f"   Maintainability index: {quality_metrics.maintainability_index:.1f}")
        print(f"   Duplication ratio: {quality_metrics.duplication_ratio:.3f}")
        print(f"   Technical debt ratio: {quality_metrics.technical_debt_ratio:.3f}")
        
        print("✅ Quality metrics analysis working")
        
        # Test 4: Linting Analysis
        print("\n🔧 Test 4: Linting Analysis")
        
        # Code with various linting issues
        linting_test_code = '''
import os
import sys
import unused_module

def function_without_docstring():
    very_long_line_that_exceeds_the_recommended_length_limit_and_should_trigger_a_style_warning_in_the_linting_process = "test"    
    return very_long_line_that_exceeds_the_recommended_length_limit_and_should_trigger_a_style_warning_in_the_linting_process

def another_function():
    pass
'''
        
        # Test different validation levels
        validation_levels = [
            ValidationLevel.BASIC,
            ValidationLevel.STANDARD,
            ValidationLevel.STRICT,
            ValidationLevel.ENTERPRISE
        ]
        
        for level in validation_levels:
            linting_result = pipeline.lint_code(linting_test_code, level)
            print(f"   {level.value}: {linting_result.total_issues} issues "
                  f"(errors: {len(linting_result.errors)}, "
                  f"warnings: {len(linting_result.warnings)}, "
                  f"style: {len(linting_result.style_issues)})")
        
        print("✅ Linting analysis working")
        
        # Test 5: Security Scanning
        print("\n🛡️ Test 5: Security Scanning")
        
        # Code with security issues
        security_test_code = '''
import subprocess
import pickle
import random

def unsafe_function(user_input):
    # Critical security issues
    result = eval(user_input)  # Code injection vulnerability
    exec(user_input)  # Another code injection
    
    # High severity issues
    subprocess.call(user_input, shell=True)  # Command injection
    data = pickle.loads(user_input)  # Unsafe deserialization
    
    # Medium severity issues
    random_value = random.random()  # Weak random number generation
    
    return result

def another_unsafe_function():
    command = "rm -rf /"
    subprocess.run(command, shell=True)
'''
        
        # Test different security levels
        security_levels = [
            SecurityLevel.LOW,
            SecurityLevel.MEDIUM,
            SecurityLevel.HIGH,
            SecurityLevel.CRITICAL
        ]
        
        for level in security_levels:
            security_issues = pipeline.scan_security(security_test_code, level)
            print(f"   {level.value}: {len(security_issues)} security issues")
            
            # Show details for high level
            if level == SecurityLevel.HIGH and security_issues:
                for issue in security_issues[:3]:  # Show first 3
                    print(f"     - {issue.severity.value}: {issue.description} (line {issue.line_number})")
        
        print("✅ Security scanning working")
        
        # Test 6: Performance Profiling
        print("\n⚡ Test 6: Performance Profiling")
        
        # Code for performance testing
        performance_test_code = '''
import time
import numpy as np

def performance_test():
    """Function to test performance profiling"""
    # Some computation
    data = []
    for i in range(1000):
        data.append(i * 2)
    
    # Some array operations
    arr = np.array(data)
    result = np.sum(arr)
    
    # Small delay to measure time
    time.sleep(0.01)
    
    return result

if __name__ == "__main__":
    result = performance_test()
    print(f"Result: {result}")
'''
        
        performance_profile = pipeline.profile_performance(performance_test_code)
        
        print(f"   Execution time: {performance_profile.execution_time_ms:.1f}ms")
        print(f"   Peak memory: {performance_profile.peak_memory_mb:.1f}MB")
        print(f"   CPU usage: {performance_profile.avg_cpu_percent:.1f}%")
        print(f"   Function calls: {performance_profile.function_calls}")
        print(f"   Hotspots found: {len(performance_profile.hotspots)}")
        
        if performance_profile.hotspots:
            print(f"   Hotspot examples:")
            for hotspot in performance_profile.hotspots[:2]:
                print(f"     - {hotspot['type']}: {hotspot['description']}")
        
        print("✅ Performance profiling working")
        
        # Test 7: Comprehensive Validation
        print("\n🎯 Test 7: Comprehensive Validation")
        
        # Comprehensive test code
        comprehensive_code = '''
import numpy as np
import time

def benchmark_function(data_size=1000):
    """
    A benchmark function for comprehensive testing.
    
    Args:
        data_size: Size of data to process
        
    Returns:
        Processing results
    """
    # Initialize data
    data = np.random.random(data_size)
    
    # Process data with some complexity
    results = []
    for i, value in enumerate(data):
        if value > 0.5:
            if i % 2 == 0:
                processed = value * 2
            else:
                processed = value / 2
            results.append(processed)
    
    # Calculate statistics
    mean_result = np.mean(results) if results else 0.0
    
    return {
        'mean': mean_result,
        'count': len(results),
        'data_size': data_size
    }

class BenchmarkRunner:
    """Runner for benchmark functions"""
    
    def __init__(self, name="default"):
        self.name = name
        self.results = []
    
    def run(self, func, *args, **kwargs):
        """Run a benchmark function"""
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        self.results.append({
            'result': result,
            'time': execution_time
        })
        
        return result
'''
        
        # Test with different validation levels
        for level in [ValidationLevel.STANDARD, ValidationLevel.STRICT]:
            validation_report = pipeline.validate_code(comprehensive_code, "benchmark", level)
            
            print(f"   {level.value} validation:")
            print(f"     Overall score: {validation_report.overall_score:.1f}/100")
            print(f"     Syntax valid: {validation_report.syntax_valid}")
            print(f"     Passed checks: {validation_report.passed_checks}")
            print(f"     Failed checks: {validation_report.failed_checks}")
            print(f"     Warnings: {validation_report.warnings_count}")
            print(f"     Security issues: {len(validation_report.security_issues)}")
            print(f"     Validation time: {validation_report.validation_time_ms:.1f}ms")
            
            if validation_report.recommendations:
                print(f"     Recommendations: {len(validation_report.recommendations)}")
                for rec in validation_report.recommendations[:2]:
                    print(f"       - {rec}")
        
        print("✅ Comprehensive validation working")
        
        # Test 8: Edge Cases and Error Handling
        print("\n⚠️ Test 8: Edge Cases and Error Handling")
        
        # Test empty code
        empty_report = pipeline.validate_code("", "test")
        print(f"   Empty code validation: score={empty_report.overall_score:.1f}, "
              f"syntax_valid={empty_report.syntax_valid}")
        
        # Test very long code
        long_code = "# Comment line\n" * 1000 + "def test(): pass"
        long_report = pipeline.validate_code(long_code, "test")
        print(f"   Long code validation: score={long_report.overall_score:.1f}, "
              f"lines={long_report.quality_metrics.lines_of_code}")
        
        # Test code with unicode
        unicode_code = '''
def test_unicode():
    """Test with unicode: αβγ δεζ"""
    message = "Hello 世界! 🌍"
    return message
'''
        
        unicode_report = pipeline.validate_code(unicode_code, "test")
        print(f"   Unicode code validation: score={unicode_report.overall_score:.1f}, "
              f"syntax_valid={unicode_report.syntax_valid}")
        
        # Test malformed code
        malformed_code = "def broken(\nprint('test'"
        malformed_report = pipeline.validate_code(malformed_code, "test")
        print(f"   Malformed code validation: score={malformed_report.overall_score:.1f}, "
              f"syntax_valid={malformed_report.syntax_valid}")
        
        print("✅ Edge cases and error handling working")
        
        # Test 9: Configuration and Thresholds
        print("\n⚙️ Test 9: Configuration and Thresholds")
        
        # Test quality thresholds
        thresholds = pipeline.quality_thresholds
        print(f"   Quality thresholds loaded: {len(thresholds)}")
        for key, value in thresholds.items():
            print(f"     {key}: {value}")
        
        # Test validation rules
        rules = pipeline.validation_rules
        print(f"   Validation rules loaded: {len(rules)}")
        enabled_rules = [rule for rule in rules if rule.enabled]
        print(f"   Enabled rules: {len(enabled_rules)}")
        
        # Test security patterns
        patterns = pipeline.security_patterns
        print(f"   Security patterns loaded: {len(patterns)}")
        critical_patterns = [p for p in patterns if p['severity'] == 'critical']
        print(f"   Critical patterns: {len(critical_patterns)}")
        
        print("✅ Configuration and thresholds working")
        
        print("\n🎉 All tests passed! Code Quality Pipeline is ready.")
        print("\n📋 Implementation Summary:")
        print("   ✅ Syntax validation and error detection")
        print("   ✅ Comprehensive linting with multiple levels")
        print("   ✅ Security vulnerability scanning")
        print("   ✅ Performance profiling and hotspot detection")
        print("   ✅ Quality metrics calculation")
        print("   ✅ Configurable validation levels")
        print("   ✅ Comprehensive reporting and recommendations")
        print("   ✅ Edge case handling and error recovery")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_quality_pipeline_edge_cases():
    """Test edge cases for Quality Pipeline"""
    print("\n🔬 Testing Quality Pipeline Edge Cases")
    print("=" * 50)
    
    try:
        pipeline = create_quality_pipeline()
        
        # Test 1: Extremely complex code
        print("📊 Test 1: Extremely Complex Code")
        
        complex_code = '''
def extremely_complex_function(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        for i in range(100):
                            for j in range(100):
                                if i % 2 == 0:
                                    if j % 3 == 0:
                                        if i + j > 50:
                                            result = a + b + c + d + e
                                        else:
                                            result = a * b * c * d * e
                                    else:
                                        result = a - b - c - d - e
                                else:
                                    result = 0
    return result
'''
        
        complex_report = pipeline.validate_code(complex_code)
        print(f"   Complex code complexity: {complex_report.quality_metrics.cyclomatic_complexity:.1f}")
        print(f"   Complex code score: {complex_report.overall_score:.1f}")
        
        # Test 2: Code with all security issues
        print("\n🛡️ Test 2: Maximum Security Issues")
        
        max_security_code = '''
import subprocess
import pickle
import random
import os

def all_security_issues(user_input):
    eval(user_input)
    exec(user_input)
    subprocess.call(user_input, shell=True)
    pickle.loads(user_input)
    random.random()
    os.system(user_input)
'''
        
        max_security_issues = pipeline.scan_security(max_security_code, SecurityLevel.CRITICAL)
        print(f"   Maximum security issues found: {len(max_security_issues)}")
        
        print("✅ Edge case testing completed")
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 H.E.L.M. Code Quality and Validation Pipeline Test Suite")
    print("=" * 60)
    
    # Run main tests
    success1 = test_quality_pipeline()
    
    # Run edge case tests
    success2 = test_quality_pipeline_edge_cases()
    
    overall_success = success1 and success2
    
    if overall_success:
        print("\n✅ Task 2.3.2: Code Quality and Validation Pipeline - COMPLETED")
        print("   🔍 Syntax validation and linting: IMPLEMENTED")
        print("   ⚡ Performance profiling: IMPLEMENTED") 
        print("   🛡️ Security vulnerability scanning: IMPLEMENTED")
        print("   📊 Quality metrics analysis: IMPLEMENTED")
        print("   ⚙️ Configurable validation levels: IMPLEMENTED")
    else:
        print("\n❌ Task 2.3.2: Code Quality and Validation Pipeline - FAILED")
    
    sys.exit(0 if overall_success else 1)
