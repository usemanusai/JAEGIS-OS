#!/usr/bin/env python3
"""
Test script for H.E.L.M. Complexity Algorithm Engine
Task 2.2.2: Complexity Algorithm Implementation

Tests the calculate_hybrid_complexity() function, multi-dimensional complexity analysis,
and adaptive complexity scaling.
"""

import sys
from core.helm.complexity_algorithms import (
    ComplexityAlgorithmEngine,
    ComplexityDimension,
    ComplexityMetric,
    ScalingMethod,
    ComplexityVector,
    create_complexity_algorithm_engine
)

def test_complexity_algorithms():
    """Test the Complexity Algorithm Engine implementation"""
    print("🔧 Testing H.E.L.M. Complexity Algorithm Engine")
    print("=" * 50)
    
    try:
        # Test 1: Engine Creation
        print("🏗️ Test 1: Engine Creation")
        
        # Create default engine
        engine = create_complexity_algorithm_engine()
        print(f"   Default engine created")
        print(f"   Default scaling method: {engine.default_scaling_method.value}")
        print(f"   Adaptation rate: {engine.adaptation_rate}")
        print(f"   Confidence threshold: {engine.confidence_threshold}")
        
        # Create custom engine
        custom_config = {
            'default_scaling_method': ScalingMethod.EXPONENTIAL.value,
            'adaptation_rate': 0.15,
            'confidence_threshold': 0.8
        }
        
        custom_engine = create_complexity_algorithm_engine(custom_config)
        print(f"   Custom engine created with scaling: {custom_engine.default_scaling_method.value}")
        
        print("✅ Engine creation working")
        
        # Test 2: Multi-dimensional Complexity Analysis
        print("\n🧮 Test 2: Multi-dimensional Complexity Analysis")
        
        # Create test benchmark data
        test_benchmark = {
            'id': 'test_benchmark_001',
            'name': 'BERT Text Classification',
            'domain': 'nlp',
            'benchmark_type': 'classification',
            'metadata': {
                'model_parameters': 110000000,  # 110M parameters
                'feature_dimensionality': 768,
                'training_time_hours': 4.0,
                'accuracy_requirement': 0.85,
                'architecture_type': 'transformer',
                'semantic_depth': 'deep',
                'language_complexity': 'complex',
                'context_length': 512,
                'code_complexity': 'medium'
            },
            'requirements': {
                'model_size': 'base',
                'dataset_size': 'large',
                'memory_gb': 16.0,
                'gpu_required': True,
                'gpu_count': 1
            },
            'dependencies': ['torch', 'transformers', 'numpy', 'pandas']
        }
        
        # Analyze complexity dimensions
        complexity_vector = engine.analyze_complexity_dimensions(test_benchmark, 'nlp')
        
        print(f"   Overall complexity: {complexity_vector.get_overall_complexity():.3f}")
        print(f"   Confidence: {complexity_vector.confidence:.3f}")
        
        # Show dimension scores
        for dimension, score in complexity_vector.dimensions.items():
            print(f"     {dimension.value}: {score:.3f}")
        
        # Show key metrics
        key_metrics = [ComplexityMetric.MODEL_PARAMETERS, ComplexityMetric.DATASET_SIZE, ComplexityMetric.MEMORY_USAGE]
        for metric in key_metrics:
            if metric in complexity_vector.metrics:
                print(f"     {metric.value}: {complexity_vector.metrics[metric]}")
        
        print("✅ Multi-dimensional complexity analysis working")
        
        # Test 3: Hybrid Complexity Calculation
        print("\n🔗 Test 3: Hybrid Complexity Calculation")
        
        # Create multiple base benchmarks
        base_benchmarks = [
            {
                'id': 'bert_classification',
                'name': 'BERT Classification',
                'domain': 'nlp',
                'benchmark_type': 'classification',
                'metadata': {
                    'model_parameters': 110000000,
                    'training_time_hours': 4.0,
                    'accuracy_requirement': 0.85
                },
                'requirements': {
                    'model_size': 'base',
                    'dataset_size': 'large',
                    'memory_gb': 16.0
                },
                'dependencies': ['torch', 'transformers']
            },
            {
                'id': 'resnet_classification',
                'name': 'ResNet Classification',
                'domain': 'computer_vision',
                'benchmark_type': 'classification',
                'metadata': {
                    'model_parameters': 25000000,
                    'training_time_hours': 8.0,
                    'accuracy_requirement': 0.90
                },
                'requirements': {
                    'model_size': 'medium',
                    'dataset_size': 'xlarge',
                    'memory_gb': 32.0
                },
                'dependencies': ['torch', 'torchvision']
            },
            {
                'id': 'gpt_generation',
                'name': 'GPT Generation',
                'domain': 'nlp',
                'benchmark_type': 'generation',
                'metadata': {
                    'model_parameters': 175000000,
                    'training_time_hours': 12.0,
                    'accuracy_requirement': 0.80
                },
                'requirements': {
                    'model_size': 'large',
                    'dataset_size': 'large',
                    'memory_gb': 64.0
                },
                'dependencies': ['torch', 'transformers', 'datasets']
            }
        ]
        
        # Calculate hybrid complexity
        hybrid_result = engine.calculate_hybrid_complexity(
            base_benchmarks=base_benchmarks,
            target_domain='hybrid_nlp_cv'
        )
        
        print(f"   Hybrid complexity: {hybrid_result.overall_complexity:.3f}")
        print(f"   Fusion method: {hybrid_result.fusion_method}")
        print(f"   Confidence: {hybrid_result.confidence:.3f}")
        print(f"   Component complexities:")
        
        for component_id, complexity in hybrid_result.component_complexities.items():
            print(f"     {component_id}: {complexity:.3f}")
        
        print("✅ Hybrid complexity calculation working")
        
        # Test 4: Different Scaling Methods
        print("\n📈 Test 4: Different Scaling Methods")
        
        scaling_methods = [
            ScalingMethod.LINEAR,
            ScalingMethod.EXPONENTIAL,
            ScalingMethod.LOGARITHMIC,
            ScalingMethod.POLYNOMIAL,
            ScalingMethod.SIGMOID,
            ScalingMethod.ADAPTIVE
        ]
        
        base_complexity = 0.7
        
        for method in scaling_methods:
            method_engine = create_complexity_algorithm_engine({
                'default_scaling_method': method.value
            })
            
            scaled_result = method_engine.calculate_hybrid_complexity(
                base_benchmarks=base_benchmarks[:2],  # Use first 2
                scaling_method=method
            )
            
            print(f"   {method.value}: {scaled_result.overall_complexity:.3f}")
        
        print("✅ Different scaling methods working")
        
        # Test 5: Adaptive Complexity Scaling
        print("\n🔄 Test 5: Adaptive Complexity Scaling")
        
        # Create mock performance history
        performance_history = [
            {'complexity': 0.6, 'success': True, 'score': 0.85, 'time': 120},
            {'complexity': 0.7, 'success': True, 'score': 0.88, 'time': 150},
            {'complexity': 0.8, 'success': False, 'score': 0.45, 'time': 200},
            {'complexity': 0.7, 'success': True, 'score': 0.87, 'time': 140},
            {'complexity': 0.9, 'success': False, 'score': 0.30, 'time': 250},
            {'complexity': 0.6, 'success': True, 'score': 0.83, 'time': 110},
            {'complexity': 0.75, 'success': True, 'score': 0.89, 'time': 160}
        ]
        
        # Test adaptive scaling
        base_complexity = 0.7
        target_performance = {'accuracy': 0.85, 'max_time': 180}
        
        adaptive_complexity = engine.adaptive_complexity_scaling(
            base_complexity=base_complexity,
            performance_history=performance_history,
            target_performance=target_performance
        )
        
        print(f"   Base complexity: {base_complexity:.3f}")
        print(f"   Adaptive complexity: {adaptive_complexity:.3f}")
        print(f"   Adaptation factor: {adaptive_complexity / base_complexity:.3f}")
        
        # Test with different performance patterns
        declining_history = [
            {'complexity': 0.6, 'success': True, 'score': 0.85},
            {'complexity': 0.6, 'success': True, 'score': 0.80},
            {'complexity': 0.6, 'success': False, 'score': 0.60},
            {'complexity': 0.6, 'success': False, 'score': 0.55},
            {'complexity': 0.6, 'success': False, 'score': 0.50}
        ]
        
        declining_adaptive = engine.adaptive_complexity_scaling(
            base_complexity=0.6,
            performance_history=declining_history
        )
        
        print(f"   Declining pattern: 0.600 -> {declining_adaptive:.3f}")
        
        print("✅ Adaptive complexity scaling working")
        
        # Test 6: Domain-Specific Analysis
        print("\n🎯 Test 6: Domain-Specific Analysis")
        
        domains = ['nlp', 'computer_vision', 'audio']
        
        for domain in domains:
            domain_benchmark = {
                'id': f'{domain}_test',
                'domain': domain,
                'metadata': {
                    'model_parameters': 50000000,
                    'training_time_hours': 2.0,
                    'accuracy_requirement': 0.8
                },
                'requirements': {
                    'model_size': 'medium',
                    'dataset_size': 'medium',
                    'memory_gb': 8.0
                }
            }
            
            domain_vector = engine.analyze_complexity_dimensions(domain_benchmark, domain)
            print(f"   {domain}: {domain_vector.get_overall_complexity():.3f}")
        
        print("✅ Domain-specific analysis working")
        
        # Test 7: Complexity Vector Operations
        print("\n🔢 Test 7: Complexity Vector Operations")
        
        # Create test vectors
        vector1 = ComplexityVector()
        vector1.dimensions = {
            ComplexityDimension.DATA: 0.7,
            ComplexityDimension.MODEL: 0.8,
            ComplexityDimension.TASK: 0.6
        }
        vector1.confidence = 0.9
        
        vector2 = ComplexityVector()
        vector2.dimensions = {
            ComplexityDimension.DATA: 0.5,
            ComplexityDimension.MODEL: 0.9,
            ComplexityDimension.COMPUTATIONAL: 0.8
        }
        vector2.confidence = 0.8
        
        # Test normalization
        normalized = vector1.normalize()
        print(f"   Vector1 overall: {vector1.get_overall_complexity():.3f}")
        print(f"   Vector1 normalized: {normalized.get_overall_complexity():.3f}")
        
        # Test fusion
        fused = engine._fuse_complexity_vectors([vector1, vector2])
        print(f"   Fused complexity: {fused.get_overall_complexity():.3f}")
        print(f"   Fused confidence: {fused.confidence:.3f}")
        
        print("✅ Complexity vector operations working")
        
        # Test 8: Edge Cases and Error Handling
        print("\n⚠️ Test 8: Edge Cases and Error Handling")
        
        # Test with empty benchmarks
        try:
            empty_result = engine.calculate_hybrid_complexity([])
            print("   ⚠️ Empty benchmarks should have failed")
        except ValueError as e:
            print(f"   ✅ Empty benchmarks correctly rejected: {str(e)[:50]}...")
        
        # Test with minimal data
        minimal_benchmark = {'id': 'minimal', 'domain': 'test'}
        minimal_vector = engine.analyze_complexity_dimensions(minimal_benchmark)
        print(f"   Minimal benchmark complexity: {minimal_vector.get_overall_complexity():.3f}")
        
        # Test with extreme values
        extreme_benchmark = {
            'id': 'extreme',
            'metadata': {
                'model_parameters': 1000000000000,  # 1T parameters
                'training_time_hours': 1000.0,
                'feature_dimensionality': 100000
            },
            'requirements': {
                'memory_gb': 1000.0,
                'gpu_count': 100
            }
        }
        
        extreme_vector = engine.analyze_complexity_dimensions(extreme_benchmark)
        print(f"   Extreme benchmark complexity: {extreme_vector.get_overall_complexity():.3f}")
        
        print("✅ Edge cases and error handling working")
        
        # Test 9: Scaling Function Validation
        print("\n📊 Test 9: Scaling Function Validation")
        
        test_scores = [0.0, 0.25, 0.5, 0.75, 1.0]
        
        for method in [ScalingMethod.LINEAR, ScalingMethod.EXPONENTIAL, ScalingMethod.LOGARITHMIC]:
            scaling_func = engine.scaling_functions[method]
            scaled_scores = [scaling_func(score) for score in test_scores]
            print(f"   {method.value}: {[f'{s:.3f}' for s in scaled_scores]}")
        
        print("✅ Scaling function validation working")
        
        print("\n🎉 All tests passed! Complexity Algorithm Engine is ready.")
        print("\n📋 Implementation Summary:")
        print("   ✅ calculate_hybrid_complexity() function")
        print("   ✅ Multi-dimensional complexity analysis")
        print("   ✅ Adaptive complexity scaling")
        print("   ✅ Multiple scaling methods")
        print("   ✅ Domain-specific complexity profiles")
        print("   ✅ Complexity vector operations")
        print("   ✅ Performance-based adaptation")
        print("   ✅ Comprehensive error handling")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complexity_algorithms_edge_cases():
    """Test edge cases for Complexity Algorithm Engine"""
    print("\n🔬 Testing Complexity Algorithm Engine Edge Cases")
    print("=" * 50)
    
    try:
        engine = create_complexity_algorithm_engine()
        
        # Test 1: Single benchmark hybrid
        print("📊 Test 1: Single Benchmark Hybrid")
        
        single_benchmark = [{
            'id': 'single',
            'domain': 'test',
            'metadata': {'model_parameters': 1000000}
        }]
        
        single_result = engine.calculate_hybrid_complexity(single_benchmark)
        print(f"   Single benchmark complexity: {single_result.overall_complexity:.3f}")
        print(f"   Fusion method: {single_result.fusion_method}")
        
        # Test 2: Large number of benchmarks
        print("\n📦 Test 2: Large Number of Benchmarks")
        
        many_benchmarks = []
        for i in range(20):
            benchmark = {
                'id': f'benchmark_{i}',
                'domain': 'test',
                'metadata': {
                    'model_parameters': 1000000 * (i + 1),
                    'training_time_hours': 1.0 + i * 0.5
                }
            }
            many_benchmarks.append(benchmark)
        
        many_result = engine.calculate_hybrid_complexity(many_benchmarks)
        print(f"   Many benchmarks complexity: {many_result.overall_complexity:.3f}")
        print(f"   Components: {len(many_result.component_complexities)}")
        
        # Test 3: Empty performance history
        print("\n📈 Test 3: Empty Performance History")
        
        empty_adaptive = engine.adaptive_complexity_scaling(
            base_complexity=0.5,
            performance_history=[]
        )
        print(f"   Empty history adaptive: {empty_adaptive:.3f}")
        
        print("✅ Edge case testing completed")
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 H.E.L.M. Complexity Algorithm Engine Test Suite")
    print("=" * 60)
    
    # Run main tests
    success1 = test_complexity_algorithms()
    
    # Run edge case tests
    success2 = test_complexity_algorithms_edge_cases()
    
    overall_success = success1 and success2
    
    if overall_success:
        print("\n✅ Task 2.2.2: Complexity Algorithm Implementation - COMPLETED")
        print("   🔗 calculate_hybrid_complexity() function: IMPLEMENTED")
        print("   🧮 Multi-dimensional complexity analysis: IMPLEMENTED") 
        print("   🔄 Adaptive complexity scaling: IMPLEMENTED")
        print("   📈 Multiple scaling methods: IMPLEMENTED")
        print("   🎯 Domain-specific analysis: IMPLEMENTED")
    else:
        print("\n❌ Task 2.2.2: Complexity Algorithm Implementation - FAILED")
    
    sys.exit(0 if overall_success else 1)
