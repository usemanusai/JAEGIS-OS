#!/usr/bin/env python3
"""
Simple test for H.E.L.M. Composer Agent
Task 2.1.1: Composer Agent Implementation - Simple Verification
"""

import sys
import asyncio
from core.agents.system.composer_agent import (
    ComposerAgent,
    CompositionRequest,
    CompositionPriority,
    create_composer_agent
)

async def test_composer_basic():
    """Basic test of Composer Agent functionality"""
    print("🔧 Testing H.E.L.M. Composer Agent (Basic)")
    print("=" * 50)
    
    try:
        # Test 1: Create agent
        print("🏗️ Test 1: Agent Creation")
        agent = create_composer_agent(agent_id="test_agent")
        print(f"   Agent created: {agent.agent_id}")
        
        # Test 2: Start agent
        print("\n🔄 Test 2: Agent Start")
        await agent.start()
        print("   Agent started successfully")
        
        # Test 3: Submit composition
        print("\n📝 Test 3: Submit Composition")
        request = CompositionRequest(
            request_id="test_001",
            name="Test Benchmark",
            description="Simple test benchmark",
            complexity_target=0.5,
            domain="test",
            priority=CompositionPriority.HIGH
        )
        
        request_id = await agent.submit_composition(request)
        print(f"   Composition submitted: {request_id}")
        
        # Test 4: Check status
        print("\n📊 Test 4: Check Status")
        await asyncio.sleep(1)  # Wait a moment
        
        status = await agent.get_composition_status(request_id)
        if status:
            print(f"   Status: {status.status.value}")
            print(f"   Progress: {status.progress_percent:.1f}%")
        
        # Test 5: Get statistics
        print("\n📈 Test 5: Agent Statistics")
        stats = agent.get_agent_statistics()
        print(f"   Total compositions: {stats['total_compositions']}")
        print(f"   Active compositions: {stats['active_compositions']}")
        
        # Test 6: Stop agent
        print("\n🛑 Test 6: Agent Stop")
        await agent.stop()
        print("   Agent stopped successfully")
        
        print("\n✅ All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 H.E.L.M. Composer Agent Basic Test")
    print("=" * 50)
    
    success = asyncio.run(test_composer_basic())
    
    if success:
        print("\n✅ Task 2.1.1: Composer Agent Implementation - BASIC VERIFICATION PASSED")
    else:
        print("\n❌ Task 2.1.1: Composer Agent Implementation - BASIC VERIFICATION FAILED")
    
    sys.exit(0 if success else 1)
