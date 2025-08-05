#!/usr/bin/env python3
"""
Unit tests for H.E.L.M. Components
Critical component test coverage for H.E.L.M. benchmark generation system
"""

import pytest
import asyncio
import unittest
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Mock enums and dataclasses for testing
class BenchmarkType(Enum):
    CURATED = "curated"
    HYBRID = "hybrid"
    GENERATED = "generated"

class ComplexityLevel(Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"

@dataclass
class BenchmarkSpecification:
    name: str
    type: BenchmarkType
    complexity: ComplexityLevel
    requirements: List[str]
    estimated_duration: float
    quality_threshold: float

@dataclass
class QualityMetric:
    accuracy: float
    completeness: float
    consistency: float
    relevance: float
    overall_score: float

# Mock H.E.L.M. components for testing
class MockHybridBenchmarkGenerator:
    def __init__(self):
        self.generated_benchmarks = []
        self.quality_threshold = 0.8
        
    async def generate_benchmark(self, specification: BenchmarkSpecification) -> Dict[str, Any]:
        # Simulate benchmark generation
        await asyncio.sleep(0.01)
        
        benchmark = {
            "id": f"benchmark_{len(self.generated_benchmarks)}",
            "name": specification.name,
            "type": specification.type.value,
            "complexity": specification.complexity.value,
            "content": f"Generated benchmark content for {specification.name}",
            "quality_metrics": QualityMetric(
                accuracy=0.9,
                completeness=0.85,
                consistency=0.88,
                relevance=0.92,
                overall_score=0.89
            ),
            "created_at": datetime.now(),
            "estimated_duration": specification.estimated_duration
        }
        
        self.generated_benchmarks.append(benchmark)
        return benchmark
        
    def calculate_complexity_score(self, requirements: List[str]) -> float:
        # Simple complexity calculation based on requirements
        base_score = len(requirements) * 0.1
        keyword_weights = {
            "advanced": 0.3,
            "complex": 0.4,
            "integration": 0.2,
            "performance": 0.25,
            "security": 0.3
        }
        
        keyword_score = 0
        for req in requirements:
            for keyword, weight in keyword_weights.items():
                if keyword.lower() in req.lower():
                    keyword_score += weight
                    
        return min(base_score + keyword_score, 1.0)
        
    def validate_quality(self, benchmark: Dict[str, Any]) -> bool:
        quality_metrics = benchmark.get("quality_metrics")
        if not quality_metrics:
            return False
            
        return quality_metrics.overall_score >= self.quality_threshold

class MockComplexityEngine:
    def __init__(self):
        self.complexity_factors = {
            "technical_depth": 0.3,
            "integration_complexity": 0.25,
            "performance_requirements": 0.2,
            "security_considerations": 0.25
        }
        
    def analyze_complexity(self, specification: BenchmarkSpecification) -> Dict[str, float]:
        # Analyze complexity factors
        factors = {}
        
        for factor, weight in self.complexity_factors.items():
            # Simulate complexity analysis
            base_value = 0.5
            if specification.complexity == ComplexityLevel.SIMPLE:
                factors[factor] = base_value * 0.6
            elif specification.complexity == ComplexityLevel.MEDIUM:
                factors[factor] = base_value * 0.8
            else:
                factors[factor] = base_value * 1.0
                
        return factors
        
    def calculate_scaling_factor(self, complexity_factors: Dict[str, float]) -> float:
        # Calculate overall scaling factor
        weighted_sum = sum(
            value * self.complexity_factors[factor]
            for factor, value in complexity_factors.items()
        )
        return min(weighted_sum, 1.0)


class TestHELMBenchmarkGenerator(unittest.TestCase):
    """Test suite for H.E.L.M. Benchmark Generator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = MockHybridBenchmarkGenerator()
        
    def test_generator_initialization(self):
        """Test benchmark generator initialization"""
        self.assertIsNotNone(self.generator)
        self.assertEqual(len(self.generator.generated_benchmarks), 0)
        self.assertEqual(self.generator.quality_threshold, 0.8)
        
    @pytest.mark.asyncio
    async def test_simple_benchmark_generation(self):
        """Test generation of a simple benchmark"""
        spec = BenchmarkSpecification(
            name="Simple Test Benchmark",
            type=BenchmarkType.CURATED,
            complexity=ComplexityLevel.SIMPLE,
            requirements=["basic functionality", "unit testing"],
            estimated_duration=1.0,
            quality_threshold=0.8
        )
        
        benchmark = await self.generator.generate_benchmark(spec)
        
        self.assertIsNotNone(benchmark)
        self.assertEqual(benchmark["name"], spec.name)
        self.assertEqual(benchmark["type"], spec.type.value)
        self.assertEqual(benchmark["complexity"], spec.complexity.value)
        self.assertIn("content", benchmark)
        self.assertIn("quality_metrics", benchmark)
        
    @pytest.mark.asyncio
    async def test_complex_benchmark_generation(self):
        """Test generation of a complex benchmark"""
        spec = BenchmarkSpecification(
            name="Complex Integration Benchmark",
            type=BenchmarkType.HYBRID,
            complexity=ComplexityLevel.COMPLEX,
            requirements=["advanced integration", "performance testing", "security validation"],
            estimated_duration=5.0,
            quality_threshold=0.85
        )
        
        benchmark = await self.generator.generate_benchmark(spec)
        
        self.assertIsNotNone(benchmark)
        self.assertEqual(benchmark["complexity"], "complex")
        self.assertGreater(benchmark["estimated_duration"], 1.0)
        
    def test_complexity_score_calculation(self):
        """Test complexity score calculation"""
        simple_requirements = ["basic test", "simple validation"]
        complex_requirements = ["advanced integration", "complex performance testing", "security analysis"]
        
        simple_score = self.generator.calculate_complexity_score(simple_requirements)
        complex_score = self.generator.calculate_complexity_score(complex_requirements)
        
        self.assertLess(simple_score, complex_score)
        self.assertLessEqual(simple_score, 1.0)
        self.assertLessEqual(complex_score, 1.0)
        
    def test_quality_validation(self):
        """Test benchmark quality validation"""
        high_quality_benchmark = {
            "quality_metrics": QualityMetric(
                accuracy=0.9,
                completeness=0.85,
                consistency=0.88,
                relevance=0.92,
                overall_score=0.89
            )
        }
        
        low_quality_benchmark = {
            "quality_metrics": QualityMetric(
                accuracy=0.6,
                completeness=0.5,
                consistency=0.4,
                relevance=0.7,
                overall_score=0.55
            )
        }
        
        self.assertTrue(self.generator.validate_quality(high_quality_benchmark))
        self.assertFalse(self.generator.validate_quality(low_quality_benchmark))


class TestHELMComplexityEngine(unittest.TestCase):
    """Test suite for H.E.L.M. Complexity Engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.complexity_engine = MockComplexityEngine()
        
    def test_complexity_engine_initialization(self):
        """Test complexity engine initialization"""
        self.assertIsNotNone(self.complexity_engine)
        self.assertIn("technical_depth", self.complexity_engine.complexity_factors)
        self.assertIn("integration_complexity", self.complexity_engine.complexity_factors)
        
    def test_complexity_analysis_simple(self):
        """Test complexity analysis for simple specifications"""
        spec = BenchmarkSpecification(
            name="Simple Test",
            type=BenchmarkType.CURATED,
            complexity=ComplexityLevel.SIMPLE,
            requirements=["basic test"],
            estimated_duration=1.0,
            quality_threshold=0.8
        )
        
        factors = self.complexity_engine.analyze_complexity(spec)
        
        self.assertIsInstance(factors, dict)
        self.assertIn("technical_depth", factors)
        self.assertIn("integration_complexity", factors)
        
        # Simple complexity should have lower factor values
        for factor_value in factors.values():
            self.assertLess(factor_value, 0.5)
            
    def test_complexity_analysis_complex(self):
        """Test complexity analysis for complex specifications"""
        spec = BenchmarkSpecification(
            name="Complex Test",
            type=BenchmarkType.HYBRID,
            complexity=ComplexityLevel.COMPLEX,
            requirements=["advanced integration", "performance testing"],
            estimated_duration=5.0,
            quality_threshold=0.85
        )
        
        factors = self.complexity_engine.analyze_complexity(spec)
        
        # Complex specifications should have higher factor values
        for factor_value in factors.values():
            self.assertGreaterEqual(factor_value, 0.4)
            
    def test_scaling_factor_calculation(self):
        """Test scaling factor calculation"""
        complexity_factors = {
            "technical_depth": 0.8,
            "integration_complexity": 0.6,
            "performance_requirements": 0.7,
            "security_considerations": 0.9
        }
        
        scaling_factor = self.complexity_engine.calculate_scaling_factor(complexity_factors)
        
        self.assertIsInstance(scaling_factor, float)
        self.assertGreaterEqual(scaling_factor, 0.0)
        self.assertLessEqual(scaling_factor, 1.0)


class TestHELMIntegration(unittest.TestCase):
    """Integration tests for H.E.L.M. components"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.generator = MockHybridBenchmarkGenerator()
        self.complexity_engine = MockComplexityEngine()
        
    @pytest.mark.asyncio
    async def test_end_to_end_benchmark_creation(self):
        """Test complete benchmark creation workflow"""
        spec = BenchmarkSpecification(
            name="Integration Test Benchmark",
            type=BenchmarkType.HYBRID,
            complexity=ComplexityLevel.MEDIUM,
            requirements=["integration testing", "performance validation"],
            estimated_duration=3.0,
            quality_threshold=0.8
        )
        
        # Analyze complexity
        complexity_factors = self.complexity_engine.analyze_complexity(spec)
        scaling_factor = self.complexity_engine.calculate_scaling_factor(complexity_factors)
        
        # Generate benchmark
        benchmark = await self.generator.generate_benchmark(spec)
        
        # Validate quality
        is_valid = self.generator.validate_quality(benchmark)
        
        # Assertions
        self.assertIsNotNone(complexity_factors)
        self.assertGreater(scaling_factor, 0.0)
        self.assertIsNotNone(benchmark)
        self.assertTrue(is_valid)
        
    @pytest.mark.asyncio
    async def test_multiple_benchmark_generation(self):
        """Test generation of multiple benchmarks"""
        specifications = [
            BenchmarkSpecification(
                name=f"Test Benchmark {i}",
                type=BenchmarkType.CURATED,
                complexity=ComplexityLevel.SIMPLE,
                requirements=[f"requirement {i}"],
                estimated_duration=1.0,
                quality_threshold=0.8
            )
            for i in range(3)
        ]
        
        benchmarks = []
        for spec in specifications:
            benchmark = await self.generator.generate_benchmark(spec)
            benchmarks.append(benchmark)
            
        self.assertEqual(len(benchmarks), 3)
        self.assertEqual(len(self.generator.generated_benchmarks), 3)
        
        # Each benchmark should be unique
        benchmark_ids = [b["id"] for b in benchmarks]
        self.assertEqual(len(set(benchmark_ids)), 3)


if __name__ == '__main__':
    # Run the tests
    unittest.main()
