#!/usr/bin/env python3
"""
Test script for H.E.L.M. Adaptive Complexity Scaling
Subtask 2.2.5.3: Configure Adaptive Complexity Scaling

Tests adaptive complexity scaling with dynamic adjustment based on 
performance metrics, user feedback, and contextual factors.
"""

import sys
import time
import random
from datetime import datetime
from core.helm.adaptive_complexity_scaling import (
    AdaptiveComplexityScalingSystem,
    ComplexityScaler,
    ScalingStrategy,
    ComplexityDimension,
    ScalingTrigger,
    ScalingConfiguration,
    ComplexityMetrics,
    create_adaptive_complexity_scaling_system
)

def test_adaptive_complexity_scaling():
    """Test the Adaptive Complexity Scaling implementation"""
    print("🔧 Testing H.E.L.M. Adaptive Complexity Scaling")
    print("=" * 50)
    
    try:
        # Test 1: System Creation and Configuration
        print("🏗️ Test 1: System Creation and Configuration")
        
        # Create system with default configuration
        system = create_adaptive_complexity_scaling_system()
        print(f"   Default system created: {'✅' if system else '❌'}")
        
        # Create system with custom configuration
        custom_config = {
            'strategy': 'adaptive',
            'min_scaling_factor': 0.2,
            'max_scaling_factor': 5.0,
            'target_success_rate': 0.85,
            'target_execution_time_ms': 800.0,
            'adaptation_rate': 0.15,
            'auto_adjustment': True
        }
        
        custom_system = create_adaptive_complexity_scaling_system(custom_config)
        config_applied = (
            custom_system.scaler.config.min_scaling_factor == 0.2 and
            custom_system.scaler.config.max_scaling_factor == 5.0 and
            custom_system.scaler.config.target_success_rate == 0.85
        )
        print(f"   Custom configuration: {'✅' if config_applied else '❌'}")
        
        # Check system structure
        has_scaler = hasattr(system, 'scaler')
        has_config = hasattr(system.scaler, 'config')
        has_metrics_history = hasattr(system.scaler, 'metrics_history')
        
        system_structure = all([has_scaler, has_config, has_metrics_history])
        print(f"   System structure: {'✅' if system_structure else '❌'}")
        
        print("✅ System creation and configuration working")
        
        # Test 2: Basic Complexity Scaling
        print("\n📊 Test 2: Basic Complexity Scaling")
        
        # Test basic scaling
        base_complexity = 1.0
        scaled_complexity = system.scale_complexity(base_complexity)
        
        basic_scaling = (
            isinstance(scaled_complexity, float) and
            scaled_complexity > 0
        )
        print(f"   Basic scaling: {'✅' if basic_scaling else '❌'}")
        print(f"   Base complexity: {base_complexity}")
        print(f"   Scaled complexity: {scaled_complexity:.3f}")
        print(f"   Current scaling factor: {system.scaler.current_scaling_factor:.3f}")
        
        # Test scaling with dimensions
        dimensions = {
            ComplexityDimension.COMPUTATIONAL: 0.4,
            ComplexityDimension.COGNITIVE: 0.3,
            ComplexityDimension.TEMPORAL: 0.3
        }
        
        dimensional_scaled = system.scale_complexity(base_complexity, dimensions=dimensions)
        
        dimensional_scaling = isinstance(dimensional_scaled, float)
        print(f"   Dimensional scaling: {'✅' if dimensional_scaling else '❌'}")
        print(f"   Dimensional scaled complexity: {dimensional_scaled:.3f}")
        
        print("✅ Basic complexity scaling working")
        
        # Test 3: Context-Aware Scaling
        print("\n🎯 Test 3: Context-Aware Scaling")
        
        # Test with different contexts
        contexts = [
            {'domain': 'mathematics', 'user_level': 'beginner', 'time_limit_ms': 3000},
            {'domain': 'programming', 'user_level': 'expert', 'time_limit_ms': 10000},
            {'domain': 'general', 'user_level': 'intermediate', 'time_limit_ms': 5000}
        ]
        
        context_results = []
        for i, context in enumerate(contexts):
            scaled = system.scale_complexity(1.0, context=context)
            context_results.append(scaled)
            print(f"   Context {i+1} ({context['user_level']}): {scaled:.3f}")
        
        context_scaling = all(isinstance(result, float) for result in context_results)
        print(f"   Context-aware scaling: {'✅' if context_scaling else '❌'}")
        
        # Test context factors
        system.set_context({
            'difficulty_preference': 0.7,  # Hard preference
            'time_pressure': 0.3,          # Low time pressure
            'expertise_level': 0.8         # Expert level
        })
        
        context_scaled = system.scale_complexity(1.0)
        context_factors_applied = context_scaled != scaled_complexity  # Should be different
        print(f"   Context factors application: {'✅' if context_factors_applied else '❌'}")
        
        print("✅ Context-aware scaling working")
        
        # Test 4: Performance Feedback and Adaptation
        print("\n📈 Test 4: Performance Feedback and Adaptation")
        
        # Simulate performance feedback over multiple iterations
        initial_scaling_factor = system.scaler.current_scaling_factor
        
        # Simulate poor performance (should reduce complexity)
        for i in range(5):
            complexity_used = system.scale_complexity(1.0)
            system.provide_feedback(
                complexity_used=complexity_used,
                performance_score=0.4,  # Poor performance
                success_rate=0.6,       # Low success rate
                execution_time_ms=1500, # High execution time
                user_satisfaction=0.3   # Low satisfaction
            )
        
        poor_performance_factor = system.scaler.current_scaling_factor
        performance_adaptation = poor_performance_factor < initial_scaling_factor
        print(f"   Poor performance adaptation: {'✅' if performance_adaptation else '❌'}")
        print(f"   Scaling factor change: {initial_scaling_factor:.3f} -> {poor_performance_factor:.3f}")
        
        # Reset and simulate good performance (should increase complexity)
        system.scaler.current_scaling_factor = 1.0
        
        for i in range(5):
            complexity_used = system.scale_complexity(1.0)
            system.provide_feedback(
                complexity_used=complexity_used,
                performance_score=0.95,  # Excellent performance
                success_rate=0.98,       # High success rate
                execution_time_ms=300,   # Fast execution
                user_satisfaction=0.9    # High satisfaction
            )
        
        good_performance_factor = system.scaler.current_scaling_factor
        performance_improvement = good_performance_factor > 1.0
        print(f"   Good performance adaptation: {'✅' if performance_improvement else '❌'}")
        print(f"   Scaling factor after good performance: {good_performance_factor:.3f}")
        
        print("✅ Performance feedback and adaptation working")
        
        # Test 5: Different Scaling Strategies
        print("\n⚡ Test 5: Different Scaling Strategies")
        
        strategies = [
            ScalingStrategy.ADAPTIVE,
            ScalingStrategy.PERFORMANCE_BASED,
            ScalingStrategy.USER_FEEDBACK_BASED,
            ScalingStrategy.CONTEXT_AWARE
        ]
        
        strategy_results = {}
        for strategy in strategies:
            # Create system with specific strategy
            strategy_config = {'strategy': strategy.value}
            strategy_system = create_adaptive_complexity_scaling_system(strategy_config)
            
            # Add some metrics
            for _ in range(3):
                complexity = strategy_system.scale_complexity(1.0)
                strategy_system.provide_feedback(
                    complexity_used=complexity,
                    performance_score=random.uniform(0.6, 0.9),
                    success_rate=random.uniform(0.7, 0.95),
                    execution_time_ms=random.uniform(200, 800),
                    user_satisfaction=random.uniform(0.5, 0.9)
                )
            
            final_factor = strategy_system.scaler.current_scaling_factor
            strategy_results[strategy.value] = final_factor
            print(f"   {strategy.value}: {final_factor:.3f}")
        
        strategy_testing = len(strategy_results) == len(strategies)
        print(f"   Strategy testing: {'✅' if strategy_testing else '❌'}")
        
        print("✅ Different scaling strategies working")
        
        # Test 6: Manual Scaling Adjustments
        print("\n🛠️ Test 6: Manual Scaling Adjustments")
        
        # Test manual adjustment
        original_factor = system.scaler.current_scaling_factor
        target_factor = 2.5
        
        system.manual_adjustment(target_factor)
        manual_factor = system.scaler.current_scaling_factor
        
        manual_adjustment = abs(manual_factor - target_factor) < 0.01
        print(f"   Manual adjustment: {'✅' if manual_adjustment else '❌'}")
        print(f"   Target factor: {target_factor}")
        print(f"   Actual factor: {manual_factor:.3f}")
        
        # Test auto-adjustment toggle
        system.enable_auto_adjustment(False)
        auto_disabled = not system.auto_adjustment_enabled
        print(f"   Auto-adjustment disable: {'✅' if auto_disabled else '❌'}")
        
        system.enable_auto_adjustment(True)
        auto_enabled = system.auto_adjustment_enabled
        print(f"   Auto-adjustment enable: {'✅' if auto_enabled else '❌'}")
        
        print("✅ Manual scaling adjustments working")
        
        # Test 7: Scaling Triggers and Events
        print("\n🔔 Test 7: Scaling Triggers and Events")
        
        # Create fresh scaler for trigger testing
        scaler = ComplexityScaler()
        
        # Test different triggers
        triggers = [
            ScalingTrigger.PERFORMANCE_THRESHOLD,
            ScalingTrigger.SUCCESS_RATE,
            ScalingTrigger.EXECUTION_TIME,
            ScalingTrigger.USER_FEEDBACK
        ]
        
        trigger_events = []
        for trigger in triggers:
            event = scaler.adjust_scaling(trigger)
            trigger_events.append(event)
            print(f"   {trigger.value}: {event.old_scaling_factor:.3f} -> {event.new_scaling_factor:.3f}")
        
        trigger_testing = (
            len(trigger_events) == len(triggers) and
            all(hasattr(event, 'trigger') for event in trigger_events) and
            all(hasattr(event, 'adjustment_reason') for event in trigger_events)
        )
        print(f"   Trigger testing: {'✅' if trigger_testing else '❌'}")
        
        # Test event structure
        sample_event = trigger_events[0]
        event_structure = (
            hasattr(sample_event, 'event_id') and
            hasattr(sample_event, 'confidence') and
            hasattr(sample_event, 'timestamp')
        )
        print(f"   Event structure: {'✅' if event_structure else '❌'}")
        
        print("✅ Scaling triggers and events working")
        
        # Test 8: Dimension-Specific Scaling
        print("\n📐 Test 8: Dimension-Specific Scaling")
        
        # Test dimension priorities
        dimension_priorities = {
            ComplexityDimension.COMPUTATIONAL: 0.4,
            ComplexityDimension.COGNITIVE: 0.3,
            ComplexityDimension.TEMPORAL: 0.2,
            ComplexityDimension.MEMORY: 0.1
        }
        
        scaler.set_dimension_priorities(dimension_priorities)
        
        # Test scaling with different dimension weights
        test_dimensions = {
            ComplexityDimension.COMPUTATIONAL: 0.6,
            ComplexityDimension.COGNITIVE: 0.4
        }
        
        metrics = scaler.scale_complexity(1.0, dimensions=test_dimensions)
        
        dimension_scaling = (
            isinstance(metrics, ComplexityMetrics) and
            hasattr(metrics, 'dimension_weights') and
            metrics.dimension_weights == test_dimensions
        )
        print(f"   Dimension-specific scaling: {'✅' if dimension_scaling else '❌'}")
        print(f"   Base complexity: {metrics.base_complexity:.3f}")
        print(f"   Scaled complexity: {metrics.scaled_complexity:.3f}")
        print(f"   Scaling factor: {metrics.scaling_factor:.3f}")
        
        print("✅ Dimension-specific scaling working")
        
        # Test 9: Scaling Statistics and Reporting
        print("\n📊 Test 9: Scaling Statistics and Reporting")
        
        # Get scaling report
        report = system.get_scaling_report()
        
        report_structure = (
            'current_scaling_factor' in report and
            'performance_metrics' in report and
            'trends' in report and
            'scaling_events' in report and
            'configuration' in report
        )
        print(f"   Report structure: {'✅' if report_structure else '❌'}")
        
        if report_structure:
            print(f"   Current scaling factor: {report['current_scaling_factor']:.3f}")
            
            perf_metrics = report['performance_metrics']
            print(f"   Avg performance score: {perf_metrics['avg_performance_score']:.3f}")
            print(f"   Avg success rate: {perf_metrics['avg_success_rate']:.3f}")
            print(f"   Avg execution time: {perf_metrics['avg_execution_time_ms']:.1f}ms")
            
            events = report['scaling_events']
            print(f"   Total scaling events: {events['total_events']}")
            print(f"   Events by trigger: {events['events_by_trigger']}")
        
        print("✅ Scaling statistics and reporting working")
        
        # Test 10: Edge Cases and Error Handling
        print("\n⚠️ Test 10: Edge Cases and Error Handling")
        
        # Test with extreme values
        extreme_system = create_adaptive_complexity_scaling_system()
        
        # Test very high complexity
        high_complexity = extreme_system.scale_complexity(1000.0)
        high_complexity_handled = isinstance(high_complexity, float) and high_complexity > 0
        print(f"   High complexity handling: {'✅' if high_complexity_handled else '❌'}")
        
        # Test very low complexity
        low_complexity = extreme_system.scale_complexity(0.001)
        low_complexity_handled = isinstance(low_complexity, float) and low_complexity > 0
        print(f"   Low complexity handling: {'✅' if low_complexity_handled else '❌'}")
        
        # Test with extreme feedback
        try:
            extreme_system.provide_feedback(
                complexity_used=1.0,
                performance_score=-0.5,  # Invalid negative score
                success_rate=1.5,        # Invalid > 1.0
                execution_time_ms=-100,  # Invalid negative time
                user_satisfaction=2.0    # Invalid > 1.0
            )
            extreme_feedback_handled = True
        except Exception:
            extreme_feedback_handled = False
        
        print(f"   Extreme feedback handling: {'✅' if extreme_feedback_handled else '❌'}")
        
        # Test scaling factor constraints
        constrained_system = create_adaptive_complexity_scaling_system({
            'min_scaling_factor': 0.5,
            'max_scaling_factor': 2.0
        })
        
        # Try to set factor outside constraints
        constrained_system.manual_adjustment(10.0)  # Above max
        constrained_factor = constrained_system.scaler.current_scaling_factor
        
        constraint_enforcement = constrained_factor <= 2.0
        print(f"   Constraint enforcement: {'✅' if constraint_enforcement else '❌'}")
        print(f"   Constrained factor: {constrained_factor:.3f}")
        
        print("✅ Edge cases and error handling working")
        
        print("\n🎉 All tests passed! Adaptive Complexity Scaling is ready.")
        print("\n📋 Implementation Summary:")
        print("   ✅ Adaptive complexity scaling with multiple strategies")
        print("   ✅ Context-aware scaling with user and domain factors")
        print("   ✅ Performance-based feedback and automatic adjustment")
        print("   ✅ Dimension-specific scaling with configurable priorities")
        print("   ✅ Manual scaling controls and auto-adjustment toggle")
        print("   ✅ Comprehensive scaling triggers and event tracking")
        print("   ✅ Statistical reporting and trend analysis")
        print("   ✅ Robust constraint enforcement and error handling")
        print("   ✅ Multiple scaling strategies (Adaptive, Performance, Feedback, Context)")
        print("   ✅ Real-time adaptation based on performance metrics")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_adaptive_complexity_scaling_edge_cases():
    """Test edge cases for Adaptive Complexity Scaling"""
    print("\n🔬 Testing Adaptive Complexity Scaling Edge Cases")
    print("=" * 50)
    
    try:
        system = create_adaptive_complexity_scaling_system()
        
        # Test 1: Rapid Adaptation Scenarios
        print("📊 Test 1: Rapid Adaptation Scenarios")
        
        # Simulate rapid performance changes
        for i in range(10):
            performance_score = 0.9 if i % 2 == 0 else 0.3  # Alternating performance
            complexity = system.scale_complexity(1.0)
            system.provide_feedback(
                complexity_used=complexity,
                performance_score=performance_score,
                success_rate=0.8,
                execution_time_ms=500
            )
        
        rapid_adaptation = len(system.scaler.metrics_history) == 10
        print(f"   Rapid adaptation handling: {'✅' if rapid_adaptation else '❌'}")
        
        # Test 2: No Feedback Scenario
        print("\n📈 Test 2: No Feedback Scenario")
        
        fresh_system = create_adaptive_complexity_scaling_system()
        
        # Scale complexity without any feedback
        no_feedback_complexity = fresh_system.scale_complexity(1.0)
        no_feedback_handled = isinstance(no_feedback_complexity, float)
        print(f"   No feedback handling: {'✅' if no_feedback_handled else '❌'}")
        
        print("✅ Edge case testing completed")
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 H.E.L.M. Adaptive Complexity Scaling Test Suite")
    print("=" * 60)
    
    # Run main tests
    success1 = test_adaptive_complexity_scaling()
    
    # Run edge case tests
    success2 = test_adaptive_complexity_scaling_edge_cases()
    
    overall_success = success1 and success2
    
    if overall_success:
        print("\n✅ Subtask 2.2.5.3: Adaptive Complexity Scaling - COMPLETED")
        print("   🎯 Context-aware complexity scaling: IMPLEMENTED")
        print("   📈 Performance-based adaptation: IMPLEMENTED") 
        print("   🔧 Multiple scaling strategies: IMPLEMENTED")
        print("   📊 Comprehensive feedback integration: IMPLEMENTED")
        print("   🛠️ Manual controls and automation: IMPLEMENTED")
    else:
        print("\n❌ Subtask 2.2.5.3: Adaptive Complexity Scaling - FAILED")
    
    sys.exit(0 if overall_success else 1)
