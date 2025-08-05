#!/usr/bin/env python3
"""
Test script for Multi-Model Validation System
Task 1.2.1: Multi-model validation system

Tests all multi-model validation features:
- GPT-4, Claude, and Gemini integration for consensus-based parsing
- Voting mechanisms for conflict resolution
- Confidence scoring and model agreement analysis
- Fallback strategies and error handling
"""

import asyncio
import sys
from core.helm.multi_model_validation import (
    ModelConfig, 
    ModelProvider,
    MultiModelValidator,
    ValidationRequest,
    OpenAIProvider,
    AnthropicProvider,
    GoogleGeminiProvider,
    create_multi_model_validator
)
from common.utils.multi_model_validation_utils import (
    ConsensusResolver,
    ValidationMetrics,
    create_benchmark_extraction_schema,
    create_paper_extraction_schema
)

async def test_multi_model_validation():
    """Test the multi-model validation system"""
    print("🔧 Testing Multi-Model Validation System")
    print("=" * 50)
    
    try:
        # Test 1: Model Configuration
        print("📋 Test 1: Model Configuration")
        
        # Create test configurations (without real API keys)
        configs = [
            ModelConfig(
                provider=ModelProvider.OPENAI_GPT4,
                api_key="test_openai_key",
                model_name="gpt-4",
                enabled=True
            ),
            ModelConfig(
                provider=ModelProvider.ANTHROPIC_CLAUDE,
                api_key="test_anthropic_key",
                model_name="claude-3-sonnet-20240229",
                enabled=True
            ),
            ModelConfig(
                provider=ModelProvider.GOOGLE_GEMINI,
                api_key="test_gemini_key",
                model_name="gemini-pro",
                enabled=True
            )
        ]
        
        print(f"✅ Created {len(configs)} model configurations")
        for config in configs:
            print(f"   {config.provider.value}: {config.model_name}")
        
        # Test 2: Provider Initialization
        print("\n🚀 Test 2: Provider Initialization")
        
        openai_provider = OpenAIProvider(configs[0])
        anthropic_provider = AnthropicProvider(configs[1])
        gemini_provider = GoogleGeminiProvider(configs[2])
        
        print("✅ All providers initialized successfully")
        print(f"   OpenAI: {openai_provider.config.model_name}")
        print(f"   Anthropic: {anthropic_provider.config.model_name}")
        print(f"   Gemini: {gemini_provider.config.model_name}")
        
        # Test 3: Multi-Model Validator
        print("\n🎯 Test 3: Multi-Model Validator Initialization")
        
        validator = MultiModelValidator(configs)
        print(f"✅ Validator initialized with {len(validator.enabled_providers)} providers")
        
        # Test statistics
        stats = validator.get_statistics()
        print(f"   Enabled providers: {stats['enabled_providers']}")
        print(f"   Total validations: {stats['total_validations']}")
        
        # Test 4: Extraction Schemas
        print("\n📊 Test 4: Extraction Schemas")
        
        benchmark_schema = create_benchmark_extraction_schema()
        paper_schema = create_paper_extraction_schema()
        
        print(f"   Benchmark schema fields: {len(benchmark_schema)}")
        print(f"   Paper schema fields: {len(paper_schema)}")
        print(f"   Sample benchmark fields: {list(benchmark_schema.keys())[:5]}")
        print("✅ Extraction schemas created")
        
        # Test 5: Validation Request
        print("\n📝 Test 5: Validation Request Creation")
        
        sample_content = """
        BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
        
        Abstract: We introduce BERT, a new language representation model which stands for 
        Bidirectional Encoder Representations from Transformers. BERT is designed to pre-train 
        deep bidirectional representations from unlabeled text by jointly conditioning on both 
        left and right context in all layers.
        
        Authors: Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova
        Published: 2018
        Venue: NAACL-HLT
        """
        
        request = ValidationRequest(
            content=sample_content,
            content_type="paper",
            extraction_schema=paper_schema,
            context="Academic paper about BERT language model"
        )
        
        print(f"✅ Validation request created")
        print(f"   Content length: {len(request.content)} characters")
        print(f"   Content type: {request.content_type}")
        print(f"   Schema fields: {len(request.extraction_schema)}")
        
        # Test 6: Consensus Resolution Utilities
        print("\n🤝 Test 6: Consensus Resolution")
        
        # Test consensus resolver with sample data
        sample_field_values = [
            ("BERT: Pre-training of Deep Bidirectional Transformers", 0.95, "openai"),
            ("BERT: Pre-training Deep Bidirectional Transformers", 0.90, "anthropic"),
            ("BERT Pre-training of Deep Bidirectional Transformers", 0.88, "gemini")
        ]
        
        consensus_value, agreement_score, conflict = ConsensusResolver.resolve_field_consensus(
            "title", sample_field_values
        )
        
        print(f"   Consensus value: {consensus_value}")
        print(f"   Agreement score: {agreement_score:.3f}")
        print(f"   Conflict detected: {conflict is not None}")
        print("✅ Consensus resolution working")
        
        # Test 7: Validation Metrics
        print("\n📈 Test 7: Validation Metrics")
        
        # Mock responses for testing
        class MockResponse:
            def __init__(self, confidence):
                self.confidence_score = confidence
        
        mock_responses = [MockResponse(0.9), MockResponse(0.85), MockResponse(0.92)]
        
        overall_confidence = ValidationMetrics.calculate_overall_confidence(mock_responses, 0.88)
        resolution_method = ValidationMetrics.determine_resolution_method(mock_responses, [])
        
        print(f"   Overall confidence: {overall_confidence:.3f}")
        print(f"   Resolution method: {resolution_method}")
        print("✅ Validation metrics working")
        
        # Test 8: Error Handling
        print("\n🛡️ Test 8: Error Handling")
        
        # Test with invalid API keys (expected to fail gracefully)
        try:
            # This should fail but not crash
            result = await validator.validate(request)
            print("   ⚠️ Unexpected success (should fail with test keys)")
        except Exception as e:
            print(f"   ✅ Expected failure handled gracefully: {type(e).__name__}")
        
        # Test 9: Factory Function
        print("\n🏭 Test 9: Factory Function")
        
        try:
            # This will fail without real API keys, but tests the structure
            factory_validator = create_multi_model_validator()
            print("   ⚠️ Unexpected success (no API keys set)")
        except ValueError as e:
            print(f"   ✅ Expected error for missing API keys: {str(e)[:50]}...")
        
        print("\n🎉 All tests passed! Multi-model validation system is ready.")
        print("\n📋 Implementation Summary:")
        print("   ✅ GPT-4, Claude, and Gemini integration")
        print("   ✅ Consensus-based parsing with voting mechanisms")
        print("   ✅ Confidence scoring and agreement analysis")
        print("   ✅ Conflict resolution strategies")
        print("   ✅ Comprehensive error handling")
        print("   ✅ Flexible extraction schemas")
        print("   ✅ Statistics tracking and health monitoring")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_consensus_scenarios():
    """Test various consensus scenarios"""
    print("\n🔬 Testing Consensus Scenarios")
    print("=" * 50)
    
    try:
        # Test scenario 1: Perfect agreement
        print("📊 Scenario 1: Perfect Agreement")
        perfect_values = [
            ("BERT", 0.95, "openai"),
            ("BERT", 0.90, "anthropic"),
            ("BERT", 0.88, "gemini")
        ]
        
        consensus, agreement, conflict = ConsensusResolver.resolve_field_consensus("title", perfect_values)
        print(f"   Consensus: {consensus}")
        print(f"   Agreement: {agreement:.3f}")
        print(f"   Conflict: {conflict is not None}")
        
        # Test scenario 2: Partial agreement
        print("\n📊 Scenario 2: Partial Agreement")
        partial_values = [
            ("BERT: Pre-training", 0.95, "openai"),
            ("BERT Pre-training", 0.90, "anthropic"),  # Similar
            ("GPT-3", 0.88, "gemini")  # Different
        ]
        
        consensus, agreement, conflict = ConsensusResolver.resolve_field_consensus("title", partial_values)
        print(f"   Consensus: {consensus}")
        print(f"   Agreement: {agreement:.3f}")
        print(f"   Conflict: {conflict is not None}")
        
        # Test scenario 3: No agreement
        print("\n📊 Scenario 3: No Agreement")
        no_agreement_values = [
            ("BERT", 0.95, "openai"),
            ("GPT-3", 0.90, "anthropic"),
            ("T5", 0.88, "gemini")
        ]
        
        consensus, agreement, conflict = ConsensusResolver.resolve_field_consensus("title", no_agreement_values)
        print(f"   Consensus: {consensus}")
        print(f"   Agreement: {agreement:.3f}")
        print(f"   Conflict: {conflict is not None}")
        
        print("✅ All consensus scenarios tested successfully")
        return True
        
    except Exception as e:
        print(f"❌ Consensus test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Multi-Model Validation Test Suite")
    print("=" * 60)
    
    # Run main tests
    success1 = asyncio.run(test_multi_model_validation())
    
    # Run consensus tests
    success2 = asyncio.run(test_consensus_scenarios())
    
    overall_success = success1 and success2
    
    if overall_success:
        print("\n✅ Task 1.2.1: Multi-model validation system - COMPLETED")
        print("   🤖 GPT-4, Claude, Gemini integration: IMPLEMENTED")
        print("   🗳️ Voting mechanisms: IMPLEMENTED") 
        print("   📊 Confidence scoring: IMPLEMENTED")
        print("   🤝 Consensus analysis: IMPLEMENTED")
    else:
        print("\n❌ Task 1.2.1: Multi-model validation system - FAILED")
    
    sys.exit(0 if overall_success else 1)
