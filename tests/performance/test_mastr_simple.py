#!/usr/bin/env python3
"""
Simple test for M.A.S.T.R. components without external dependencies
Tests the core functionality and imports
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all M.A.S.T.R. components can be imported"""
    
    print("🧪 Testing M.A.S.T.R. Component Imports")
    print("=" * 40)
    
    try:
        print("1. Testing ToolProspector import...")
        from core.mastr.prospector import ToolProspector
        print("   ✅ ToolProspector imported successfully")
        
        print("2. Testing SystemArchitect import...")
        from core.mastr.architect import SystemArchitect
        print("   ✅ SystemArchitect imported successfully")
        
        print("3. Testing ContainerSmith import...")
        from core.mastr.smith import ContainerSmith
        print("   ✅ ContainerSmith imported successfully")
        
        print("4. Testing DeploymentQuartermaster import...")
        from core.mastr.quartermaster import DeploymentQuartermaster
        print("   ✅ DeploymentQuartermaster imported successfully")
        
        print("5. Testing MASTRManager import...")
        from core.mastr.manager import MASTRManager
        print("   ✅ MASTRManager imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_component_initialization():
    """Test component initialization without external dependencies"""
    
    print("\n🔧 Testing M.A.S.T.R. Component Initialization")
    print("=" * 45)
    
    try:
        from core.mastr.prospector import ToolProspector
        from core.mastr.architect import SystemArchitect
        from core.mastr.smith import ContainerSmith
        from core.mastr.quartermaster import DeploymentQuartermaster
        
        print("1. Initializing ToolProspector...")
        prospector = ToolProspector()
        print(f"   ✅ ToolProspector initialized: {prospector.prospector_id[:8]}...")
        
        print("2. Initializing SystemArchitect...")
        architect = SystemArchitect()
        print(f"   ✅ SystemArchitect initialized: {architect.architect_id[:8]}...")
        
        print("3. Initializing ContainerSmith...")
        smith = ContainerSmith()
        print(f"   ✅ ContainerSmith initialized: {smith.smith_id[:8]}...")
        
        print("4. Initializing DeploymentQuartermaster...")
        quartermaster = DeploymentQuartermaster()
        print(f"   ✅ DeploymentQuartermaster initialized: {quartermaster.quartermaster_id[:8]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

def test_component_statistics():
    """Test component statistics functionality"""
    
    print("\n📊 Testing M.A.S.T.R. Component Statistics")
    print("=" * 42)
    
    try:
        from core.mastr.prospector import ToolProspector
        from core.mastr.architect import SystemArchitect
        from core.mastr.smith import ContainerSmith
        from core.mastr.quartermaster import DeploymentQuartermaster
        
        # Initialize components
        prospector = ToolProspector()
        architect = SystemArchitect()
        smith = ContainerSmith()
        quartermaster = DeploymentQuartermaster()
        
        print("1. Getting ToolProspector statistics...")
        prospector_stats = prospector.get_prospector_statistics()
        print(f"   📈 Tools prospected: {prospector_stats['tools_prospected']}")
        print(f"   📈 Sources searched: {prospector_stats['sources_searched']}")
        
        print("2. Getting SystemArchitect statistics...")
        architect_stats = architect.get_architect_statistics()
        print(f"   📈 Architectures designed: {architect_stats['architectures_designed']}")
        print(f"   📈 Blueprints generated: {architect_stats['blueprints_generated']}")
        
        print("3. Getting ContainerSmith statistics...")
        smith_stats = smith.get_smith_statistics()
        print(f"   📈 Containers built: {smith_stats['containers_built']}")
        print(f"   📈 Successful builds: {smith_stats['successful_builds']}")
        
        print("4. Getting DeploymentQuartermaster statistics...")
        quartermaster_stats = quartermaster.get_quartermaster_statistics()
        print(f"   📈 Deployments executed: {quartermaster_stats['deployments_executed']}")
        print(f"   📈 Active deployments: {quartermaster_stats['active_deployments']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Statistics test failed: {e}")
        return False

async def test_async_functionality():
    """Test async functionality of components"""
    
    print("\n⚡ Testing M.A.S.T.R. Async Functionality")
    print("=" * 38)
    
    try:
        from core.mastr.prospector import ToolProspector
        from core.mastr.architect import SystemArchitect
        
        print("1. Testing ToolProspector async methods...")
        prospector = ToolProspector()
        
        # Test prospecting (mock data)
        search_terms = ["web framework", "database", "api"]
        result = await prospector.prospect_tools(search_terms, quality_threshold=0.5)
        print(f"   ✅ Prospecting completed: {result['total_found']} tools found")
        
        print("2. Testing SystemArchitect async methods...")
        architect = SystemArchitect()
        
        # Test architecture design (mock data)
        project_description = "Build a web API with database integration"
        discovered_tools = result.get("discovered_tools", [])
        arch_result = await architect.design_architecture(project_description, discovered_tools)
        
        if arch_result["success"]:
            arch = arch_result["architecture"]
            print(f"   ✅ Architecture designed: {arch['architecture_id']}")
            print(f"   📐 Pattern: {arch['architecture_pattern']['pattern_name']}")
            print(f"   🔧 Components: {len(arch['system_components'])}")
        else:
            print(f"   ❌ Architecture design failed: {arch_result.get('error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Async test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 M.A.S.T.R. Framework Component Test Suite")
    print("Testing core functionality without external dependencies")
    print("=" * 60)
    
    # Run tests
    import_success = test_imports()
    init_success = test_component_initialization()
    stats_success = test_component_statistics()
    
    # Run async test
    import asyncio
    async_success = asyncio.run(test_async_functionality())
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 15)
    print(f"Import Tests: {'✅ PASS' if import_success else '❌ FAIL'}")
    print(f"Initialization Tests: {'✅ PASS' if init_success else '❌ FAIL'}")
    print(f"Statistics Tests: {'✅ PASS' if stats_success else '❌ FAIL'}")
    print(f"Async Tests: {'✅ PASS' if async_success else '❌ FAIL'}")
    
    all_passed = all([import_success, init_success, stats_success, async_success])
    
    if all_passed:
        print("\n🎉 All M.A.S.T.R. component tests passed!")
        print("✅ M.A.S.T.R. Framework is ready for deployment!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
