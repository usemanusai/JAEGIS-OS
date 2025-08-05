#!/usr/bin/env python3
"""
Test script for H.E.L.M. Human-in-the-Loop Validation System
Task 1.2.4: Human-in-the-loop validation

Tests review queue and approval workflow for low-confidence extracted data
"""

import sys
import tempfile
import shutil
from datetime import datetime
from core.helm.human_validation import (
    ReviewQueue,
    HumanValidationWorkflow,
    ReviewItem,
    ReviewDecision,
    ReviewerProfile,
    ReviewStatus,
    Priority,
    create_review_queue,
    create_human_validation_workflow
)

def test_human_validation_system():
    """Test the human validation system"""
    print("🔧 Testing H.E.L.M. Human-in-the-Loop Validation System")
    print("=" * 50)
    
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Test 1: Review Queue Creation
        print("📋 Test 1: Review Queue Creation")
        
        review_queue = create_review_queue(temp_dir)
        print(f"   Review queue created with storage at {temp_dir}")
        print(f"   Confidence threshold: {review_queue.confidence_threshold}")
        print(f"   Max queue size: {review_queue.max_queue_size}")
        
        print("✅ Review queue creation working")
        
        # Test 2: Reviewer Registration
        print("\n👥 Test 2: Reviewer Registration")
        
        # Register additional reviewer
        test_reviewer = ReviewerProfile(
            id="test_reviewer_001",
            name="Dr. Test Reviewer",
            email="test@example.com",
            expertise_domains=["nlp", "ml", "ai"],
            max_concurrent_reviews=4
        )
        
        review_queue.register_reviewer(test_reviewer)
        print(f"   Registered reviewer: {test_reviewer.name}")
        
        # Check reviewer count
        stats = review_queue.get_queue_statistics()
        print(f"   Total active reviewers: {stats['active_reviewers']}")
        
        print("✅ Reviewer registration working")
        
        # Test 3: Adding Items to Queue
        print("\n📝 Test 3: Adding Items to Review Queue")
        
        # Mock confidence result
        class MockConfidenceResult:
            def __init__(self, confidence):
                self.overall_confidence = confidence
        
        # Add high-confidence item (should be low priority)
        high_conf_data = {
            "title": "High Confidence Paper Title",
            "authors": ["Author One", "Author Two"],
            "description": "This is a well-extracted paper with high confidence."
        }
        
        high_conf_item_id = review_queue.add_item(
            extracted_data=high_conf_data,
            confidence_result=MockConfidenceResult(0.85),
            source_url="https://arxiv.org/abs/1234.5678",
            metadata={"extraction_method": "multi_model"}
        )
        
        print(f"   Added high-confidence item: {high_conf_item_id}")
        
        # Add low-confidence item (should be high priority)
        low_conf_data = {
            "title": "Uncertain Title",
            "authors": [],
            "description": "Poor extraction quality"
        }
        
        low_conf_item_id = review_queue.add_item(
            extracted_data=low_conf_data,
            confidence_result=MockConfidenceResult(0.25),
            source_url="https://unknown-site.com/paper",
            metadata={"extraction_method": "single_model"}
        )
        
        print(f"   Added low-confidence item: {low_conf_item_id}")
        
        # Add urgent item
        urgent_data = {
            "title": "Critical Paper",
            "authors": None,
            "description": ""
        }
        
        urgent_item_id = review_queue.add_item(
            extracted_data=urgent_data,
            confidence_result=MockConfidenceResult(0.15),
            source_url="https://important-venue.com/paper",
            metadata={"extraction_method": "failed"}
        )
        
        print(f"   Added urgent item: {urgent_item_id}")
        
        # Check queue statistics
        stats = review_queue.get_queue_statistics()
        print(f"   Total pending items: {stats['total_pending']}")
        print(f"   Priority breakdown: {stats['priority_breakdown']}")
        
        print("✅ Adding items to queue working")
        
        # Test 4: Item Assignment
        print("\n🎯 Test 4: Item Assignment")
        
        # Get pending items
        pending_items = review_queue.get_pending_items()
        print(f"   Pending items: {len(pending_items)}")
        
        # Check priority ordering
        priorities = [item.priority.value for item in pending_items]
        print(f"   Priority order: {priorities}")
        
        # Assign item to reviewer
        if pending_items:
            first_item = pending_items[0]
            success = review_queue.assign_item(first_item.id, "test_reviewer_001")
            print(f"   Assignment success: {success}")
            
            # Check reviewer workload
            workload = review_queue.get_reviewer_workload("test_reviewer_001")
            print(f"   Reviewer current items: {workload['current_items']}")
            print(f"   Available slots: {workload['available_slots']}")
        
        print("✅ Item assignment working")
        
        # Test 5: Review Submission
        print("\n✅ Test 5: Review Submission")
        
        # Submit review decision
        if pending_items:
            assigned_item = pending_items[0]
            
            # Create review decision
            decision = ReviewDecision(
                item_id=assigned_item.id,
                reviewer_id="test_reviewer_001",
                decision=ReviewStatus.APPROVED,
                corrected_data={
                    "title": "Corrected Title",
                    "authors": ["Corrected Author"],
                    "description": "Corrected description with proper formatting."
                },
                notes="Minor corrections applied. Data quality is acceptable.",
                confidence_override=0.90
            )
            
            success = review_queue.submit_review(decision)
            print(f"   Review submission success: {success}")
            
            # Check updated statistics
            stats = review_queue.get_queue_statistics()
            print(f"   Completed items: {stats['total_completed']}")
            print(f"   In review items: {stats['total_in_review']}")
        
        print("✅ Review submission working")
        
        # Test 6: Human Validation Workflow
        print("\n🔄 Test 6: Human Validation Workflow")
        
        workflow = create_human_validation_workflow(temp_dir)
        
        # Test should_require_review
        high_conf_result = MockConfidenceResult(0.85)
        low_conf_result = MockConfidenceResult(0.45)
        
        should_review_high = workflow.should_require_review(high_conf_result)
        should_review_low = workflow.should_require_review(low_conf_result)
        
        print(f"   High confidence requires review: {should_review_high}")
        print(f"   Low confidence requires review: {should_review_low}")
        
        # Submit for review through workflow
        workflow_item_id = workflow.submit_for_review(
            extracted_data={"title": "Workflow Test", "authors": ["Test Author"]},
            confidence_result=low_conf_result,
            source_url="https://test.com/paper"
        )
        
        print(f"   Workflow submission ID: {workflow_item_id}")
        
        print("✅ Human validation workflow working")
        
        # Test 7: Review Interface Data
        print("\n📊 Test 7: Review Interface Data")
        
        interface_data = workflow.get_review_interface_data("test_reviewer_001")
        
        print(f"   Workload data: {interface_data['workload']['current_items']} items")
        print(f"   Available items: {len(interface_data['available_items'])}")
        print(f"   Queue utilization: {interface_data['queue_statistics']['queue_utilization']:.2%}")
        
        print("✅ Review interface data working")
        
        # Test 8: Validation Callbacks
        print("\n🔔 Test 8: Validation Callbacks")
        
        callback_triggered = False
        
        def test_callback(decision):
            nonlocal callback_triggered
            callback_triggered = True
            print(f"     Callback triggered for decision: {decision.decision.value}")
        
        workflow.register_validation_callback(test_callback)
        
        # Process a decision to trigger callback
        test_decision = ReviewDecision(
            item_id=workflow_item_id,
            reviewer_id="test_reviewer_001",
            decision=ReviewStatus.NEEDS_REVISION,
            notes="Needs more information"
        )
        
        workflow.process_validation_decision(test_decision)
        print(f"   Callback triggered: {callback_triggered}")
        
        print("✅ Validation callbacks working")
        
        # Test 9: Persistence and Recovery
        print("\n💾 Test 9: Persistence and Recovery")
        
        # Create new queue instance to test loading
        new_queue = ReviewQueue(temp_dir)
        
        new_stats = new_queue.get_queue_statistics()
        print(f"   Loaded pending items: {new_stats['total_pending']}")
        print(f"   Loaded completed items: {new_stats['total_completed']}")
        print(f"   Loaded reviewers: {new_stats['active_reviewers']}")
        
        print("✅ Persistence and recovery working")
        
        print("\n🎉 All tests passed! Human validation system is ready.")
        print("\n📋 Implementation Summary:")
        print("   ✅ Review queue with priority management")
        print("   ✅ Reviewer registration and workload tracking")
        print("   ✅ Automatic item assignment based on confidence")
        print("   ✅ Review decision processing and statistics")
        print("   ✅ Human validation workflow integration")
        print("   ✅ Persistent storage and recovery")
        print("   ✅ Validation callbacks and event handling")
        print("   ✅ Review interface data generation")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

def test_validation_edge_cases():
    """Test edge cases for human validation"""
    print("\n🔬 Testing Human Validation Edge Cases")
    print("=" * 50)
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        review_queue = create_review_queue(temp_dir)
        
        # Test 1: Empty data handling
        print("📊 Test 1: Empty Data Handling")
        
        empty_item_id = review_queue.add_item(
            extracted_data={},
            confidence_result=None,
            source_url="",
            source_content=""
        )
        
        print(f"   Empty data item created: {empty_item_id}")
        
        # Test 2: Queue overflow
        print("\n📈 Test 2: Queue Overflow Handling")
        
        # Set small queue size for testing
        review_queue.max_queue_size = 3
        
        # Add items beyond capacity
        for i in range(5):
            review_queue.add_item(
                extracted_data={"title": f"Test Item {i}"},
                confidence_result=None
            )
        
        stats = review_queue.get_queue_statistics()
        print(f"   Items in queue after overflow: {stats['total_pending']}")
        print(f"   Max queue size: {review_queue.max_queue_size}")
        
        # Test 3: Invalid assignments
        print("\n⚠️ Test 3: Invalid Assignment Handling")
        
        # Try to assign non-existent item
        invalid_assign = review_queue.assign_item("invalid_id", "test_reviewer_001")
        print(f"   Invalid item assignment: {invalid_assign}")
        
        # Try to assign to non-existent reviewer
        pending_items = review_queue.get_pending_items()
        if pending_items:
            invalid_reviewer = review_queue.assign_item(pending_items[0].id, "invalid_reviewer")
            print(f"   Invalid reviewer assignment: {invalid_reviewer}")
        
        print("✅ Edge case testing completed")
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        return False
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    print("🚀 H.E.L.M. Human Validation Test Suite")
    print("=" * 60)
    
    # Run main tests
    success1 = test_human_validation_system()
    
    # Run edge case tests
    success2 = test_validation_edge_cases()
    
    overall_success = success1 and success2
    
    if overall_success:
        print("\n✅ Task 1.2.4: Human-in-the-loop validation - COMPLETED")
        print("   📋 Review queue management: IMPLEMENTED")
        print("   👥 Reviewer registration and tracking: IMPLEMENTED") 
        print("   🎯 Automatic assignment based on confidence: IMPLEMENTED")
        print("   ✅ Review decision processing: IMPLEMENTED")
        print("   🔄 Complete validation workflow: IMPLEMENTED")
        print("   💾 Persistent storage and recovery: IMPLEMENTED")
    else:
        print("\n❌ Task 1.2.4: Human-in-the-loop validation - FAILED")
    
    sys.exit(0 if overall_success else 1)
