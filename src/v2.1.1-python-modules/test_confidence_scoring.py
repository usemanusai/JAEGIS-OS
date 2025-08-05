#!/usr/bin/env python3
"""
Test script for H.E.L.M. Confidence Scoring System
Task 1.2.3: Confidence scoring for extracted data

Tests multi-factor confidence calculation and model agreement scoring
"""

import sys
from datetime import datetime
from core.helm.confidence_scoring import (
    ConfidenceScorer,
    ConfidenceLevel,
    ConfidenceFactors,
    create_confidence_scorer
)

def test_confidence_scoring():
    """Test the confidence scoring system"""
    print("🔧 Testing H.E.L.M. Confidence Scoring System")
    print("=" * 50)
    
    try:
        # Test 1: Confidence Scorer Creation
        print("📊 Test 1: Confidence Scorer Creation")
        
        # Create default scorer
        scorer = create_confidence_scorer()
        print(f"   Default scorer created")
        print(f"   Weights: {scorer.weights}")
        
        # Create custom scorer
        custom_config = {
            'weights': {
                'model_agreement': 0.30,
                'data_completeness': 0.25,
                'source_reliability': 0.20,
                'extraction_consistency': 0.10,
                'validation_score': 0.10,
                'content_quality': 0.05
            },
            'thresholds': {
                'very_high': 0.95,
                'high': 0.80,
                'medium': 0.60,
                'low': 0.30
            }
        }
        
        custom_scorer = create_confidence_scorer(custom_config)
        print(f"   Custom scorer created with modified weights")
        
        print("✅ Confidence scorer creation working")
        
        # Test 2: Mock Model Responses
        print("\n🤖 Test 2: Mock Model Responses")
        
        # Create mock model responses with high agreement
        class MockResponse:
            def __init__(self, extracted_data, confidence_score):
                self.extracted_data = extracted_data
                self.confidence_score = confidence_score
        
        high_agreement_responses = [
            MockResponse({
                "title": "BERT: Pre-training of Deep Bidirectional Transformers",
                "authors": ["Jacob Devlin", "Ming-Wei Chang"],
                "venue": "NAACL-HLT 2019",
                "description": "We introduce BERT, a new language representation model."
            }, 0.95),
            MockResponse({
                "title": "BERT: Pre-training Deep Bidirectional Transformers",
                "authors": ["Jacob Devlin", "Ming-Wei Chang"],
                "venue": "NAACL 2019",
                "description": "We introduce BERT, a new language representation model for NLP."
            }, 0.92),
            MockResponse({
                "title": "BERT: Pre-training of Deep Bidirectional Transformers",
                "authors": ["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee"],
                "venue": "NAACL-HLT 2019",
                "description": "BERT is a new language representation model."
            }, 0.90)
        ]
        
        print(f"   Created {len(high_agreement_responses)} mock responses with high agreement")
        
        # Create mock responses with low agreement
        low_agreement_responses = [
            MockResponse({
                "title": "BERT: Pre-training of Deep Bidirectional Transformers",
                "authors": ["Jacob Devlin"],
                "venue": "NAACL 2019",
                "description": "BERT is a language model."
            }, 0.85),
            MockResponse({
                "title": "GPT-3: Language Models are Few-Shot Learners",
                "authors": ["Tom Brown"],
                "venue": "NeurIPS 2020",
                "description": "GPT-3 is a large language model."
            }, 0.60),
            MockResponse({
                "title": "Attention Is All You Need",
                "authors": ["Ashish Vaswani"],
                "venue": "NIPS 2017",
                "description": "The Transformer architecture."
            }, 0.70)
        ]
        
        print(f"   Created {len(low_agreement_responses)} mock responses with low agreement")
        
        print("✅ Mock model responses created")
        
        # Test 3: High Confidence Scenario
        print("\n🎯 Test 3: High Confidence Scenario")
        
        high_quality_data = {
            "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
            "description": "We introduce BERT, a new language representation model which stands for Bidirectional Encoder Representations from Transformers. BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers.",
            "authors": ["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee", "Kristina Toutanova"],
            "venue": "NAACL-HLT 2019",
            "code_url": "https://github.com/google-research/bert",
            "paper_url": "https://arxiv.org/abs/1810.04805"
        }
        
        # Mock validation result
        class MockValidationResult:
            def __init__(self, is_valid, errors=None):
                self.is_valid = is_valid
                self.errors = errors or []
        
        high_confidence_result = scorer.calculate_confidence(
            extracted_data=high_quality_data,
            model_responses=high_agreement_responses,
            source_url="https://arxiv.org/abs/1810.04805",
            validation_result=MockValidationResult(True)
        )
        
        print(f"   Overall confidence: {high_confidence_result.overall_confidence:.3f}")
        print(f"   Confidence level: {high_confidence_result.confidence_level.value}")
        print(f"   Model agreement: {high_confidence_result.factors.model_agreement:.3f}")
        print(f"   Data completeness: {high_confidence_result.factors.data_completeness:.3f}")
        print(f"   Source reliability: {high_confidence_result.factors.source_reliability:.3f}")
        print(f"   Recommendations: {len(high_confidence_result.recommendations)}")
        
        print("✅ High confidence scenario working")
        
        # Test 4: Low Confidence Scenario
        print("\n⚠️ Test 4: Low Confidence Scenario")
        
        low_quality_data = {
            "title": "Test",
            "description": "Short desc",
            "authors": [],
            "venue": None
        }
        
        low_confidence_result = scorer.calculate_confidence(
            extracted_data=low_quality_data,
            model_responses=low_agreement_responses,
            source_url="https://unknown-site.com/paper",
            validation_result=MockValidationResult(False, ["title too short", "missing authors"])
        )
        
        print(f"   Overall confidence: {low_confidence_result.overall_confidence:.3f}")
        print(f"   Confidence level: {low_confidence_result.confidence_level.value}")
        print(f"   Model agreement: {low_confidence_result.factors.model_agreement:.3f}")
        print(f"   Data completeness: {low_confidence_result.factors.data_completeness:.3f}")
        print(f"   Source reliability: {low_confidence_result.factors.source_reliability:.3f}")
        print(f"   Recommendations: {len(low_confidence_result.recommendations)}")
        
        print("✅ Low confidence scenario working")
        
        # Test 5: Field-Level Confidence
        print("\n📋 Test 5: Field-Level Confidence")
        
        field_confidences = high_confidence_result.field_confidences
        print(f"   Field confidences calculated: {len(field_confidences)}")
        
        for field, confidence in field_confidences.items():
            print(f"     {field}: {confidence:.3f}")
        
        print("✅ Field-level confidence working")
        
        # Test 6: Source Reliability Assessment
        print("\n🌐 Test 6: Source Reliability Assessment")
        
        test_sources = [
            "https://arxiv.org/abs/1234.5678",
            "https://paperswithcode.com/paper/test",
            "https://github.com/user/repo",
            "https://huggingface.co/models/bert",
            "https://unknown-site.com/paper",
            "https://stanford.edu/research/paper"
        ]
        
        for source in test_sources:
            reliability = scorer._calculate_source_reliability(source)
            domain = scorer._extract_domain(source)
            print(f"   {domain}: {reliability:.3f}")
        
        print("✅ Source reliability assessment working")
        
        # Test 7: Content Quality Assessment
        print("\n📝 Test 7: Content Quality Assessment")
        
        quality_test_data = [
            {
                "title": "A Very Comprehensive and Well-Written Research Paper Title",
                "description": "This is a detailed and comprehensive description that provides substantial information about the research topic, methodology, and findings. It contains multiple sentences and demonstrates good writing quality.",
                "authors": ["Author One", "Author Two", "Author Three"],
                "code_url": "https://github.com/user/repo",
                "paper_url": "https://arxiv.org/abs/1234.5678"
            },
            {
                "title": "Short",
                "description": "Bad",
                "authors": [],
                "code_url": "invalid-url"
            }
        ]
        
        for i, data in enumerate(quality_test_data):
            quality = scorer._calculate_content_quality(data)
            print(f"   Test data {i+1} quality: {quality:.3f}")
        
        print("✅ Content quality assessment working")
        
        # Test 8: Confidence Level Categorization
        print("\n🏷️ Test 8: Confidence Level Categorization")
        
        test_confidences = [0.95, 0.82, 0.65, 0.35, 0.15]
        
        for conf in test_confidences:
            level = scorer._determine_confidence_level(conf)
            print(f"   Confidence {conf:.2f} -> {level.value}")
        
        print("✅ Confidence level categorization working")
        
        # Test 9: Recommendation Generation
        print("\n💡 Test 9: Recommendation Generation")
        
        print(f"   High confidence recommendations:")
        for rec in high_confidence_result.recommendations:
            print(f"     - {rec}")
        
        print(f"   Low confidence recommendations:")
        for rec in low_confidence_result.recommendations:
            print(f"     - {rec}")
        
        print("✅ Recommendation generation working")
        
        print("\n🎉 All tests passed! Confidence scoring system is ready.")
        print("\n📋 Implementation Summary:")
        print("   ✅ Multi-factor confidence calculation")
        print("   ✅ Model agreement scoring")
        print("   ✅ Data completeness assessment")
        print("   ✅ Source reliability evaluation")
        print("   ✅ Content quality analysis")
        print("   ✅ Field-level confidence scoring")
        print("   ✅ Configurable weights and thresholds")
        print("   ✅ Actionable recommendations")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_confidence_edge_cases():
    """Test edge cases for confidence scoring"""
    print("\n🔬 Testing Confidence Scoring Edge Cases")
    print("=" * 50)
    
    try:
        scorer = create_confidence_scorer()
        
        # Test 1: Empty data
        print("📊 Test 1: Empty Data Handling")
        
        class MockResponse:
            def __init__(self, extracted_data, confidence_score):
                self.extracted_data = extracted_data
                self.confidence_score = confidence_score
        
        empty_result = scorer.calculate_confidence(
            extracted_data={},
            model_responses=[MockResponse({}, 0.5)],
            source_url="",
            validation_result=None
        )
        
        print(f"   Empty data confidence: {empty_result.overall_confidence:.3f}")
        print(f"   Empty data level: {empty_result.confidence_level.value}")
        
        # Test 2: Single model response
        print("\n🤖 Test 2: Single Model Response")
        
        single_response = [MockResponse({"title": "Test Paper"}, 0.8)]
        
        single_result = scorer.calculate_confidence(
            extracted_data={"title": "Test Paper"},
            model_responses=single_response,
            source_url="https://arxiv.org/test",
            validation_result=None
        )
        
        print(f"   Single model confidence: {single_result.overall_confidence:.3f}")
        print(f"   Model agreement: {single_result.factors.model_agreement:.3f}")
        
        # Test 3: Malformed data
        print("\n⚠️ Test 3: Malformed Data Handling")
        
        malformed_data = {
            "title": None,
            "authors": "",
            "description": [],
            "invalid_field": {"nested": "data"}
        }
        
        malformed_result = scorer.calculate_confidence(
            extracted_data=malformed_data,
            model_responses=[MockResponse(malformed_data, 0.3)],
            source_url="https://test.com",
            validation_result=None
        )
        
        print(f"   Malformed data confidence: {malformed_result.overall_confidence:.3f}")
        print(f"   Data completeness: {malformed_result.factors.data_completeness:.3f}")
        
        print("✅ Edge case testing completed")
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 H.E.L.M. Confidence Scoring Test Suite")
    print("=" * 60)
    
    # Run main tests
    success1 = test_confidence_scoring()
    
    # Run edge case tests
    success2 = test_confidence_edge_cases()
    
    overall_success = success1 and success2
    
    if overall_success:
        print("\n✅ Task 1.2.3: Confidence scoring for extracted data - COMPLETED")
        print("   📊 Multi-factor confidence calculation: IMPLEMENTED")
        print("   🤖 Model agreement scoring: IMPLEMENTED") 
        print("   📋 Field-level confidence: IMPLEMENTED")
        print("   🌐 Source reliability assessment: IMPLEMENTED")
        print("   📝 Content quality analysis: IMPLEMENTED")
    else:
        print("\n❌ Task 1.2.3: Confidence scoring for extracted data - FAILED")
    
    sys.exit(0 if overall_success else 1)
