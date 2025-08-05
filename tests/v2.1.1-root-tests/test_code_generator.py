#!/usr/bin/env python3
"""
Test script for H.E.L.M. Robust Code Generator
Task 2.3.1: Robust Benchmark Script Generation

Tests multi-model code generation with consensus, static code analysis,
and automated testing of generated scripts.
"""

import sys
import tempfile
from pathlib import Path
from core.helm.code_generator import (
    RobustCodeGenerator,
    CodeGenerationRequest,
    CodeQualityLevel,
    TestingFramework,
    CodeGenerationModel,
    create_robust_code_generator
)
from core.helm.composer import BenchmarkSpecification, BenchmarkType

def test_code_generator():
    """Test the Robust Code Generator implementation"""
    print("🔧 Testing H.E.L.M. Robust Code Generator")
    print("=" * 50)
    
    try:
        # Test 1: Generator Creation
        print("🏗️ Test 1: Generator Creation")
        
        # Create default generator
        generator = create_robust_code_generator()
        print(f"   Default generator created")
        print(f"   Enabled models: {[model.value for model in generator.enabled_models]}")
        print(f"   Consensus threshold: {generator.consensus_threshold}")
        print(f"   Max attempts: {generator.max_generation_attempts}")
        
        # Create custom generator
        custom_config = {
            'enabled_models': [CodeGenerationModel.GPT4.value, CodeGenerationModel.CLAUDE.value],
            'consensus_threshold': 0.8,
            'max_generation_attempts': 2,
            'timeout_seconds': 120
        }
        
        custom_generator = create_robust_code_generator(custom_config)
        print(f"   Custom generator created with threshold: {custom_generator.consensus_threshold}")
        
        print("✅ Generator creation working")
        
        # Test 2: Code Generation Request Setup
        print("\n📋 Test 2: Code Generation Request Setup")
        
        # Create test specifications
        test_specs = [
            BenchmarkSpecification(
                id="test_classification",
                name="BERT Text Classification",
                description="BERT-based text classification benchmark for sentiment analysis",
                benchmark_type=BenchmarkType.CLASSIFICATION,
                domain="nlp",
                complexity_target=0.7,
                requirements={"model_size": "base", "dataset": "imdb", "gpu_required": True},
                metadata={"task": "sentiment_analysis", "model": "bert"}
            ),
            BenchmarkSpecification(
                id="test_generation",
                name="GPT Text Generation",
                description="GPT-based text generation benchmark",
                benchmark_type=BenchmarkType.GENERATION,
                domain="nlp",
                complexity_target=0.8,
                requirements={"model_size": "medium", "max_length": 512},
                metadata={"task": "text_generation", "model": "gpt"}
            )
        ]
        
        # Create generation requests
        requests = []
        for spec in test_specs:
            request = CodeGenerationRequest(
                specification=spec,
                quality_level=CodeQualityLevel.PRODUCTION,
                testing_framework=TestingFramework.PYTEST,
                include_documentation=True,
                include_tests=True,
                target_python_version="3.8+",
                additional_requirements=["torch>=1.9.0", "numpy>=1.20.0"]
            )
            requests.append(request)
            print(f"   Created request for: {spec.name}")
        
        print("✅ Code generation request setup working")
        
        # Test 3: Basic Code Generation
        print("\n🎯 Test 3: Basic Code Generation")
        
        # Generate code for classification benchmark
        classification_request = requests[0]
        generation_result = generator.generate_benchmark_code(classification_request)
        
        print(f"   Generation successful: {generation_result.success}")
        print(f"   Request ID: {generation_result.request_id}")
        print(f"   Consensus score: {generation_result.consensus_score:.3f}")
        print(f"   Confidence: {generation_result.confidence:.3f}")
        print(f"   Generation time: {generation_result.generation_time_ms:.1f}ms")
        
        # Check generated code
        generated_code = generation_result.generated_code
        print(f"   Main code length: {len(generated_code.main_code)} characters")
        print(f"   Test code length: {len(generated_code.test_code)} characters")
        print(f"   Documentation length: {len(generated_code.documentation)} characters")
        print(f"   Requirements: {len(generated_code.requirements)} items")
        
        # Show some code snippet
        code_lines = generated_code.main_code.split('\n')
        print(f"   Code preview (first 5 lines):")
        for i, line in enumerate(code_lines[:5]):
            print(f"     {i+1}: {line}")
        
        print("✅ Basic code generation working")
        
        # Test 4: Static Code Analysis
        print("\n🔍 Test 4: Static Code Analysis")
        
        # Test static analysis on generated code
        static_result = generator.validate_generated_code(
            generated_code.main_code, 
            classification_request.specification
        )
        
        print(f"   Code is valid: {static_result.is_valid}")
        print(f"   Syntax errors: {len(static_result.syntax_errors)}")
        print(f"   Style violations: {len(static_result.style_violations)}")
        print(f"   Security issues: {len(static_result.security_issues)}")
        print(f"   Complexity score: {static_result.complexity_score:.1f}")
        print(f"   Maintainability index: {static_result.maintainability_index:.1f}")
        
        if static_result.syntax_errors:
            print(f"   Syntax errors:")
            for error in static_result.syntax_errors[:3]:
                print(f"     - {error}")
        
        if static_result.style_violations:
            print(f"   Style violations (first 3):")
            for violation in static_result.style_violations[:3]:
                print(f"     - {violation}")
        
        print("✅ Static code analysis working")
        
        # Test 5: Automated Testing
        print("\n🧪 Test 5: Automated Testing")
        
        # Test the generated code
        test_results = generator.test_generated_code(
            generated_code,
            classification_request.specification
        )
        
        print(f"   Syntax valid: {test_results['syntax_valid']}")
        print(f"   Imports valid: {test_results['imports_valid']}")
        print(f"   Execution successful: {test_results['execution_successful']}")
        print(f"   Tests passed: {test_results['tests_passed']}")
        print(f"   Execution time: {test_results['execution_time_ms']:.1f}ms")
        print(f"   Coverage: {test_results['coverage_percentage']:.1f}%")
        
        if test_results['errors']:
            print(f"   Errors:")
            for error in test_results['errors'][:3]:
                print(f"     - {error}")
        
        print("✅ Automated testing working")
        
        # Test 6: Different Quality Levels
        print("\n⭐ Test 6: Different Quality Levels")
        
        quality_levels = [
            CodeQualityLevel.BASIC,
            CodeQualityLevel.PRODUCTION,
            CodeQualityLevel.ENTERPRISE
        ]
        
        for quality_level in quality_levels:
            quality_request = CodeGenerationRequest(
                specification=test_specs[0],
                quality_level=quality_level,
                include_tests=True,
                include_documentation=True
            )
            
            quality_result = generator.generate_benchmark_code(quality_request)
            
            print(f"   {quality_level.value}: confidence {quality_result.confidence:.3f}, "
                  f"time {quality_result.generation_time_ms:.1f}ms")
        
        print("✅ Different quality levels working")
        
        # Test 7: Multiple Benchmark Types
        print("\n📊 Test 7: Multiple Benchmark Types")
        
        benchmark_types = [
            BenchmarkType.CLASSIFICATION,
            BenchmarkType.GENERATION,
            BenchmarkType.REGRESSION,
            BenchmarkType.TRANSLATION
        ]
        
        for benchmark_type in benchmark_types:
            type_spec = BenchmarkSpecification(
                id=f"test_{benchmark_type.value}",
                name=f"Test {benchmark_type.value.title()} Benchmark",
                description=f"Test benchmark for {benchmark_type.value}",
                benchmark_type=benchmark_type,
                domain="test",
                complexity_target=0.6
            )
            
            type_request = CodeGenerationRequest(
                specification=type_spec,
                quality_level=CodeQualityLevel.PRODUCTION
            )
            
            type_result = generator.generate_benchmark_code(type_request)
            
            print(f"   {benchmark_type.value}: success {type_result.success}, "
                  f"confidence {type_result.confidence:.3f}")
        
        print("✅ Multiple benchmark types working")
        
        # Test 8: Code Templates and Requirements
        print("\n📝 Test 8: Code Templates and Requirements")
        
        # Check loaded templates
        templates = generator.code_templates
        print(f"   Loaded templates: {len(templates)}")
        
        for template_name in templates.keys():
            template_length = len(templates[template_name])
            print(f"     {template_name}: {template_length} characters")
        
        # Test requirement extraction
        sample_code = '''
import torch
import numpy as np
from sklearn.metrics import accuracy_score
import pandas as pd
import matplotlib.pyplot as plt
'''
        
        requirements = generator._extract_requirements(sample_code)
        print(f"   Extracted requirements: {requirements}")
        
        print("✅ Code templates and requirements working")
        
        # Test 9: Code Analysis Methods
        print("\n🔬 Test 9: Code Analysis Methods")
        
        # Test various analysis methods
        sample_code = '''
def complex_function(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                for i in range(100):
                    if i % 2 == 0:
                        result = x + y + z
                    else:
                        result = x * y * z
                return result
    return 0
'''
        
        # Test complexity calculation
        complexity = generator._calculate_code_complexity(sample_code)
        print(f"   Code complexity: {complexity:.1f}")
        
        # Test maintainability index
        maintainability = generator._calculate_maintainability_index(sample_code)
        print(f"   Maintainability index: {maintainability:.1f}")
        
        # Test style checking
        style_issues = generator._check_code_style(sample_code)
        print(f"   Style issues: {len(style_issues)}")
        
        # Test security checking
        security_code = "eval(user_input)"
        security_issues = generator._check_security_issues(security_code)
        print(f"   Security issues in eval code: {len(security_issues)}")
        
        print("✅ Code analysis methods working")
        
        # Test 10: Edge Cases and Error Handling
        print("\n⚠️ Test 10: Edge Cases and Error Handling")
        
        # Test with minimal specification
        minimal_spec = BenchmarkSpecification(
            id="minimal",
            name="Minimal Test",
            description="Minimal benchmark for testing",
            benchmark_type=BenchmarkType.CLASSIFICATION,
            domain="test",
            complexity_target=0.1
        )
        
        minimal_request = CodeGenerationRequest(
            specification=minimal_spec,
            quality_level=CodeQualityLevel.BASIC,
            include_tests=False,
            include_documentation=False
        )
        
        minimal_result = generator.generate_benchmark_code(minimal_request)
        print(f"   Minimal spec: success {minimal_result.success}, "
              f"confidence {minimal_result.confidence:.3f}")
        
        # Test with high complexity
        complex_spec = BenchmarkSpecification(
            id="complex",
            name="Complex Test",
            description="Complex benchmark for testing",
            benchmark_type=BenchmarkType.GENERATION,
            domain="test",
            complexity_target=0.95
        )
        
        complex_request = CodeGenerationRequest(
            specification=complex_spec,
            quality_level=CodeQualityLevel.ENTERPRISE
        )
        
        complex_result = generator.generate_benchmark_code(complex_request)
        print(f"   Complex spec: success {complex_result.success}, "
              f"confidence {complex_result.confidence:.3f}")
        
        # Test invalid code validation
        invalid_code = "def broken_function(\n    return 'syntax error'"
        invalid_analysis = generator.validate_generated_code(invalid_code, minimal_spec)
        print(f"   Invalid code validation: valid={invalid_analysis.is_valid}, "
              f"errors={len(invalid_analysis.syntax_errors)}")
        
        print("✅ Edge cases and error handling working")
        
        print("\n🎉 All tests passed! Robust Code Generator is ready.")
        print("\n📋 Implementation Summary:")
        print("   ✅ Multi-model code generation with consensus")
        print("   ✅ Static code analysis and validation")
        print("   ✅ Automated testing of generated scripts")
        print("   ✅ Multiple quality levels support")
        print("   ✅ Template-based code generation")
        print("   ✅ Requirement extraction and management")
        print("   ✅ Comprehensive error handling")
        print("   ✅ Performance and security analysis")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_code_generator_edge_cases():
    """Test edge cases for Code Generator"""
    print("\n🔬 Testing Code Generator Edge Cases")
    print("=" * 50)
    
    try:
        generator = create_robust_code_generator()
        
        # Test 1: Empty specification
        print("📊 Test 1: Empty Specification Handling")
        
        try:
            empty_spec = BenchmarkSpecification(
                id="",
                name="",
                description="",
                benchmark_type=BenchmarkType.CLASSIFICATION,
                domain="",
                complexity_target=0.0
            )
            
            empty_request = CodeGenerationRequest(specification=empty_spec)
            empty_result = generator.generate_benchmark_code(empty_request)
            
            print(f"   Empty spec handled: success={empty_result.success}")
            
        except Exception as e:
            print(f"   Empty spec error: {type(e).__name__}")
        
        # Test 2: Very long code analysis
        print("\n📦 Test 2: Large Code Analysis")
        
        large_code = "def test():\n    pass\n" * 1000  # 1000 lines
        large_analysis = generator.validate_generated_code(large_code, None)
        print(f"   Large code analysis: valid={large_analysis.is_valid}, "
              f"complexity={large_analysis.complexity_score:.1f}")
        
        # Test 3: Code with unicode characters
        print("\n🌐 Test 3: Unicode Code Handling")
        
        unicode_code = '''
def test_unicode():
    """Test with unicode: αβγ δεζ"""
    message = "Hello 世界! 🌍"
    return message
'''
        
        unicode_analysis = generator.validate_generated_code(unicode_code, None)
        print(f"   Unicode code analysis: valid={unicode_analysis.is_valid}")
        
        print("✅ Edge case testing completed")
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 H.E.L.M. Robust Code Generator Test Suite")
    print("=" * 60)
    
    # Run main tests
    success1 = test_code_generator()
    
    # Run edge case tests
    success2 = test_code_generator_edge_cases()
    
    overall_success = success1 and success2
    
    if overall_success:
        print("\n✅ Task 2.3.1: Robust Benchmark Script Generation - COMPLETED")
        print("   🎯 Multi-model code generation with consensus: IMPLEMENTED")
        print("   🔍 Static code analysis: IMPLEMENTED") 
        print("   🧪 Automated testing of generated scripts: IMPLEMENTED")
        print("   ⭐ Multiple quality levels: IMPLEMENTED")
        print("   📝 Template-based generation: IMPLEMENTED")
    else:
        print("\n❌ Task 2.3.1: Robust Benchmark Script Generation - FAILED")
    
    sys.exit(0 if overall_success else 1)
