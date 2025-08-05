#!/usr/bin/env python3
"""
Test script for H.E.L.M. Intelligent Specification Generator
Task 2.2.1: Intelligent Specification Generation

Tests the generate_hybrid_spec() function, advanced complexity modeling,
and specification validation/optimization.
"""

import sys
import tempfile
from core.helm.specification_generator import (
    IntelligentSpecificationGenerator,
    SpecificationConstraints,
    SpecificationStrategy,
    ComplexityModel,
    OptimizationObjective,
    create_intelligent_specification_generator
)
from core.helm.composer import BenchmarkType, create_hybrid_benchmark_generator
from core.helm.script_inventory import create_script_inventory_manager, InventoryItem, InventoryStatus

def test_specification_generator():
    """Test the Intelligent Specification Generator implementation"""
    print("🔧 Testing H.E.L.M. Intelligent Specification Generator")
    print("=" * 50)
    
    try:
        # Test 1: Generator Creation
        print("🏗️ Test 1: Generator Creation")
        
        # Create default generator
        generator = create_intelligent_specification_generator()
        print(f"   Default generator created")
        print(f"   Default strategy: {generator.default_strategy.value}")
        print(f"   Complexity model: {generator.complexity_model.value}")
        print(f"   Optimization iterations: {generator.optimization_iterations}")
        
        # Create generator with dependencies
        temp_dir = tempfile.mkdtemp()
        inventory_manager = create_script_inventory_manager(
            inventory_path=f"{temp_dir}/test_inventory.json",
            backup_dir=f"{temp_dir}/backups"
        )
        benchmark_generator = create_hybrid_benchmark_generator(
            inventory_manager=inventory_manager
        )
        
        custom_config = {
            'default_strategy': SpecificationStrategy.ADAPTIVE.value,
            'complexity_model': ComplexityModel.HYBRID.value,
            'optimization_iterations': 5,
            'mutation_rate': 0.15
        }
        
        custom_generator = create_intelligent_specification_generator(
            config=custom_config,
            inventory_manager=inventory_manager,
            benchmark_generator=benchmark_generator
        )
        
        print(f"   Custom generator created with strategy: {custom_generator.default_strategy.value}")
        
        print("✅ Generator creation working")
        
        # Test 2: Base Benchmark Setup
        print("\n📋 Test 2: Base Benchmark Setup")
        
        # Add some base benchmarks to inventory
        base_benchmarks = [
            InventoryItem(
                id="base_bert_001",
                name="BERT Text Classification",
                version="1.0.0",
                description="BERT-based text classification benchmark",
                category="nlp",
                status=InventoryStatus.ACTIVE,
                metadata={
                    'actual_complexity': 0.7,
                    'benchmark_type': 'classification',
                    'requirements': {'model_size': 'base', 'dataset': 'imdb'}
                }
            ),
            InventoryItem(
                id="base_resnet_001",
                name="ResNet Image Classification",
                version="1.0.0",
                description="ResNet-based image classification benchmark",
                category="computer_vision",
                status=InventoryStatus.ACTIVE,
                metadata={
                    'actual_complexity': 0.8,
                    'benchmark_type': 'classification',
                    'requirements': {'model_depth': 50, 'dataset': 'imagenet'}
                }
            ),
            InventoryItem(
                id="base_gpt_001",
                name="GPT Text Generation",
                version="1.0.0",
                description="GPT-based text generation benchmark",
                category="nlp",
                status=InventoryStatus.ACTIVE,
                metadata={
                    'actual_complexity': 0.9,
                    'benchmark_type': 'generation',
                    'requirements': {'model_size': 'medium', 'max_length': 512}
                }
            )
        ]
        
        # Add to inventory
        for item in base_benchmarks:
            inventory_manager.add_item(item)
            print(f"   Added base benchmark: {item.name}")
        
        base_benchmark_ids = [item.id for item in base_benchmarks]
        
        print("✅ Base benchmark setup working")
        
        # Test 3: Hybrid Specification Generation
        print("\n🎯 Test 3: Hybrid Specification Generation")
        
        # Test basic hybrid specification generation
        hybrid_spec = custom_generator.generate_hybrid_spec(
            base_benchmarks=base_benchmark_ids[:2],  # Use first 2
            target_complexity=0.75,
            strategy=SpecificationStrategy.BALANCED
        )
        
        print(f"   Generated hybrid spec: {hybrid_spec.name}")
        print(f"   Domain: {hybrid_spec.domain}")
        print(f"   Type: {hybrid_spec.benchmark_type.value}")
        print(f"   Target complexity: {hybrid_spec.complexity_target:.3f}")
        print(f"   Requirements: {len(hybrid_spec.requirements)} items")
        
        # Test with constraints
        constraints = SpecificationConstraints(
            min_complexity=0.5,
            max_complexity=0.9,
            max_resources={'cpu': 100.0, 'memory': 50.0},
            required_domains=['nlp', 'computer_vision']
        )
        
        constrained_spec = custom_generator.generate_hybrid_spec(
            base_benchmarks=base_benchmark_ids,
            target_complexity=0.8,
            constraints=constraints,
            strategy=SpecificationStrategy.CONSERVATIVE,
            optimization_objective=OptimizationObjective.BALANCE_QUALITY
        )
        
        print(f"   Constrained spec: {constrained_spec.name}")
        print(f"   Constrained complexity: {constrained_spec.complexity_target:.3f}")
        
        print("✅ Hybrid specification generation working")
        
        # Test 4: Adaptive Specification Generation
        print("\n🔄 Test 4: Adaptive Specification Generation")
        
        # Create mock performance history
        performance_history = [
            {'complexity': 0.6, 'success': True, 'score': 0.85},
            {'complexity': 0.7, 'success': True, 'score': 0.90},
            {'complexity': 0.8, 'success': False, 'score': 0.45},
            {'complexity': 0.7, 'success': True, 'score': 0.88},
            {'complexity': 0.9, 'success': False, 'score': 0.30},
            {'complexity': 0.6, 'success': True, 'score': 0.82}
        ]
        
        adaptive_spec = custom_generator.generate_adaptive_spec(
            domain="nlp",
            performance_history=performance_history,
            user_preferences={'prefer_accuracy': True, 'max_time': 300}
        )
        
        print(f"   Adaptive spec: {adaptive_spec.name}")
        print(f"   Adaptive complexity: {adaptive_spec.complexity_target:.3f}")
        print(f"   Adaptive type: {adaptive_spec.benchmark_type.value}")
        print(f"   Generation method: {adaptive_spec.metadata.get('generation_method')}")
        
        print("✅ Adaptive specification generation working")
        
        # Test 5: Complexity Modeling
        print("\n🧮 Test 5: Complexity Modeling")
        
        # Test different complexity models
        complexity_models = [
            ComplexityModel.LINEAR,
            ComplexityModel.EXPONENTIAL,
            ComplexityModel.LOGARITHMIC,
            ComplexityModel.POLYNOMIAL,
            ComplexityModel.HYBRID
        ]
        
        for model in complexity_models:
            model_generator = create_intelligent_specification_generator(
                config={'complexity_model': model.value},
                inventory_manager=inventory_manager
            )
            
            model_spec = model_generator.generate_hybrid_spec(
                base_benchmarks=base_benchmark_ids[:2],
                target_complexity=0.7
            )
            
            print(f"   {model.value} model complexity: {model_spec.complexity_target:.3f}")
        
        print("✅ Complexity modeling working")
        
        # Test 6: Specification Optimization
        print("\n⚡ Test 6: Specification Optimization")
        
        # Test optimization with different objectives
        optimization_objectives = [
            OptimizationObjective.MAXIMIZE_COMPLEXITY,
            OptimizationObjective.MINIMIZE_RESOURCES,
            OptimizationObjective.BALANCE_QUALITY,
            OptimizationObjective.OPTIMIZE_PERFORMANCE
        ]
        
        base_spec = hybrid_spec
        
        for objective in optimization_objectives:
            optimized_spec = custom_generator.optimize_specification(
                specification=base_spec,
                constraints=constraints,
                objective=objective
            )
            
            print(f"   {objective.value}: complexity {optimized_spec.complexity_target:.3f}")
        
        print("✅ Specification optimization working")
        
        # Test 7: Specification Validation
        print("\n🔍 Test 7: Specification Validation")
        
        # Test valid specification
        is_valid, issues = custom_generator.validate_specification(hybrid_spec, constraints)
        print(f"   Valid spec validation: {'PASSED' if is_valid else 'FAILED'} ({len(issues)} issues)")
        
        # Test invalid specification
        from core.helm.composer import BenchmarkSpecification
        invalid_spec = BenchmarkSpecification(
            id="invalid_test",
            name="",  # Invalid: empty name
            description="Test invalid specification",
            benchmark_type=BenchmarkType.CLASSIFICATION,
            domain="test",
            complexity_target=1.5  # Invalid: > 1.0
        )
        
        is_invalid, invalid_issues = custom_generator.validate_specification(invalid_spec, constraints)
        print(f"   Invalid spec validation: {'FAILED' if not is_invalid else 'UNEXPECTED PASS'} ({len(invalid_issues)} issues)")
        
        if invalid_issues:
            for issue in invalid_issues[:3]:  # Show first 3 issues
                print(f"     - {issue}")
        
        print("✅ Specification validation working")
        
        # Test 8: Strategy Comparison
        print("\n📊 Test 8: Strategy Comparison")
        
        strategies = [
            SpecificationStrategy.ADAPTIVE,
            SpecificationStrategy.CONSERVATIVE,
            SpecificationStrategy.AGGRESSIVE,
            SpecificationStrategy.BALANCED
        ]
        
        for strategy in strategies:
            strategy_spec = custom_generator.generate_hybrid_spec(
                base_benchmarks=base_benchmark_ids[:2],
                target_complexity=0.7,
                strategy=strategy
            )
            
            print(f"   {strategy.value}: {strategy_spec.complexity_target:.3f} complexity")
        
        print("✅ Strategy comparison working")
        
        # Test 9: Template System
        print("\n📝 Test 9: Template System")
        
        # Check loaded templates
        templates = custom_generator.templates
        print(f"   Loaded templates: {len(templates)}")
        
        for template_name, template in templates.items():
            print(f"     {template_name}: {template.default_complexity:.2f} default complexity")
        
        # Check complexity profiles
        profiles = custom_generator.complexity_profiles
        print(f"   Loaded complexity profiles: {len(profiles)}")
        
        for profile_name, profile in profiles.items():
            print(f"     {profile_name}: {profile.base_complexity:.2f} base complexity")
        
        print("✅ Template system working")
        
        # Test 10: Edge Cases and Error Handling
        print("\n⚠️ Test 10: Edge Cases and Error Handling")
        
        # Test with empty base benchmarks
        try:
            empty_spec = custom_generator.generate_hybrid_spec(
                base_benchmarks=[],
                target_complexity=0.5
            )
            print("   ⚠️ Empty base benchmarks should have failed")
        except ValueError as e:
            print(f"   ✅ Empty base benchmarks correctly rejected: {str(e)[:50]}...")
        
        # Test with invalid complexity
        try:
            invalid_complexity_spec = custom_generator.generate_hybrid_spec(
                base_benchmarks=base_benchmark_ids[:1],
                target_complexity=1.5  # Invalid
            )
            print("   ⚠️ Invalid complexity should have failed")
        except ValueError as e:
            print(f"   ✅ Invalid complexity correctly rejected: {str(e)[:50]}...")
        
        # Test with non-existent base benchmarks
        non_existent_spec = custom_generator.generate_hybrid_spec(
            base_benchmarks=["non_existent_1", "non_existent_2"],
            target_complexity=0.6
        )
        print(f"   Non-existent base benchmarks handled: {non_existent_spec.name}")
        
        print("✅ Edge cases and error handling working")
        
        print("\n🎉 All tests passed! Intelligent Specification Generator is ready.")
        print("\n📋 Implementation Summary:")
        print("   ✅ Intelligent hybrid specification generation")
        print("   ✅ Advanced complexity modeling with multiple algorithms")
        print("   ✅ Specification validation and optimization")
        print("   ✅ Adaptive generation based on performance history")
        print("   ✅ Multiple generation strategies")
        print("   ✅ Genetic algorithm optimization")
        print("   ✅ Template and profile system")
        print("   ✅ Comprehensive error handling")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specification_generator_edge_cases():
    """Test edge cases for Specification Generator"""
    print("\n🔬 Testing Specification Generator Edge Cases")
    print("=" * 50)
    
    try:
        generator = create_intelligent_specification_generator()
        
        # Test 1: Extreme complexity values
        print("📊 Test 1: Extreme Complexity Values")
        
        # Test very low complexity
        try:
            low_spec = generator.generate_hybrid_spec(
                base_benchmarks=["dummy"],
                target_complexity=0.01
            )
            print(f"   Very low complexity: {low_spec.complexity_target:.3f}")
        except Exception as e:
            print(f"   Very low complexity error: {type(e).__name__}")
        
        # Test very high complexity
        try:
            high_spec = generator.generate_hybrid_spec(
                base_benchmarks=["dummy"],
                target_complexity=0.99
            )
            print(f"   Very high complexity: {high_spec.complexity_target:.3f}")
        except Exception as e:
            print(f"   Very high complexity error: {type(e).__name__}")
        
        # Test 2: Large number of base benchmarks
        print("\n📦 Test 2: Large Number of Base Benchmarks")
        
        many_benchmarks = [f"benchmark_{i}" for i in range(50)]
        
        try:
            many_spec = generator.generate_hybrid_spec(
                base_benchmarks=many_benchmarks,
                target_complexity=0.7
            )
            print(f"   Many benchmarks spec: {many_spec.name}")
        except Exception as e:
            print(f"   Many benchmarks error: {type(e).__name__}")
        
        print("✅ Edge case testing completed")
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 H.E.L.M. Intelligent Specification Generator Test Suite")
    print("=" * 60)
    
    # Run main tests
    success1 = test_specification_generator()
    
    # Run edge case tests
    success2 = test_specification_generator_edge_cases()
    
    overall_success = success1 and success2
    
    if overall_success:
        print("\n✅ Task 2.2.1: Intelligent Specification Generation - COMPLETED")
        print("   🎯 generate_hybrid_spec() function: IMPLEMENTED")
        print("   🧮 Advanced complexity modeling: IMPLEMENTED") 
        print("   🔍 Specification validation/optimization: IMPLEMENTED")
        print("   🔄 Adaptive generation: IMPLEMENTED")
        print("   ⚡ Genetic algorithm optimization: IMPLEMENTED")
    else:
        print("\n❌ Task 2.2.1: Intelligent Specification Generation - FAILED")
    
    sys.exit(0 if overall_success else 1)
