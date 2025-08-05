#!/usr/bin/env python3
"""
JAEGIS Startup Script
====================

Simple startup script for the JAEGIS ecosystem with different modes.
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from jaegis_master import JAEGISMaster


def print_banner():
    """Print JAEGIS startup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║      ██╗ █████╗ ███████╗ ██████╗ ██╗███████╗                                ║
    ║      ██║██╔══██╗██╔════╝██╔════╝ ██║██╔════╝                                ║
    ║      ██║███████║█████╗  ██║  ███╗██║███████╗                                ║
    ║ ██   ██║██╔══██║██╔══╝  ██║   ██║██║╚════██║                                ║
    ║ ╚█████╔╝██║  ██║███████╗╚██████╔╝██║███████║                                ║
    ║  ╚════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝                                ║
    ║                                                                              ║
    ║           Just Another Extremely General Intelligence System                 ║
    ║                                                                              ║
    ║                    🤖 Autonomous AI Ecosystem 🤖                            ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


async def run_normal_mode():
    """Run JAEGIS in normal operation mode"""
    print("🚀 Starting JAEGIS in normal operation mode...")
    
    config = {
        'script': {'enable_api': True, 'api_port': 8080},
        'atlas': {'enable_api': True, 'api_port': 8081},
        'helm': {'enable_api': True, 'api_port': 8082},
        'mastr': {'enable_api': True, 'api_port': 8083},
        'ascend': {'enable_api': True, 'api_port': 8084},
        'cori': {'enable_htm': True, 'enable_cognitive_map': True},
        'cockpit': {'host': '127.0.0.1', 'port': 8090}
    }
    
    jaegis_master = JAEGISMaster(config)
    
    try:
        if not await jaegis_master.startup():
            print("❌ Failed to start JAEGIS ecosystem")
            return 1
        
        print("\n✅ JAEGIS ecosystem is now fully operational!")
        print("\n📊 Service Endpoints:")
        print("   • JAEGIS Cockpit:    http://localhost:8090")
        print("   • S.C.R.I.P.T. API:  http://localhost:8080")
        print("   • A.T.L.A.S. API:    http://localhost:8081")
        print("   • H.E.L.M. API:      http://localhost:8082")
        print("   • M.A.S.T.R. API:    http://localhost:8083")
        print("   • A.S.C.E.N.D. API:  http://localhost:8084")
        
        print("\n🎯 Available Dashboards:")
        print("   • Operations:        http://localhost:8090/")
        print("   • Forge Console:     http://localhost:8090/forge")
        print("   • Governance:        http://localhost:8090/governance")
        print("   • Treasury:          http://localhost:8090/treasury")
        
        print("\n💡 Press Ctrl+C to shutdown gracefully")
        
        # Keep running
        while True:
            await asyncio.sleep(60)
            
            # Periodic health check
            health = await jaegis_master.health_check()
            if not health['healthy']:
                print("⚠️ Warning: Some services may be unhealthy")
    
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested...")
        await jaegis_master.shutdown()
        print("✅ JAEGIS ecosystem stopped gracefully")
    except Exception as e:
        print(f"❌ Error: {e}")
        await jaegis_master.shutdown()
        return 1
    
    return 0


async def run_genesis_test():
    """Run the Genesis Test"""
    print("🧪 Starting JAEGIS Genesis Test...")
    print("   This test validates the complete autonomous capability expansion loop")
    
    config = {
        'script': {'enable_api': False},
        'atlas': {'enable_api': False},
        'helm': {'enable_api': False},
        'mastr': {'enable_api': False},
        'ascend': {'enable_api': False},
        'cori': {'enable_htm': True, 'enable_cognitive_map': True},
        'cockpit': {'enable_api': False}
    }
    
    jaegis_master = JAEGISMaster(config)
    
    try:
        if not await jaegis_master.startup():
            print("❌ Failed to start JAEGIS ecosystem for testing")
            return 1
        
        print("✅ JAEGIS ecosystem started for testing")
        print("🧪 Running Genesis Test...")
        
        # Allow services to fully initialize
        await asyncio.sleep(3)
        
        # Run the Genesis Test
        test_results = await jaegis_master.genesis_test()
        
        # Display results
        print("\n" + "="*80)
        print("🧪 GENESIS TEST RESULTS")
        print("="*80)
        print(f"Test: {test_results['test_name']}")
        print(f"Duration: {test_results.get('duration', 0):.2f} seconds")
        
        if test_results['success']:
            print("Result: ✅ PASSED - JAEGIS autonomous loop validated successfully!")
        else:
            print("Result: ❌ FAILED - Some components need attention")
        
        if test_results.get('error'):
            print(f"Error: {test_results['error']}")
        
        print("\n📋 Stage Results:")
        for stage_name, stage_data in test_results.get('stages', {}).items():
            status = "✅" if stage_data.get('detected', stage_data.get('success', True)) else "❌"
            print(f"   {status} {stage_name.replace('_', ' ').title()}")
        
        print("="*80)
        
        await jaegis_master.shutdown()
        return 0 if test_results['success'] else 1
    
    except Exception as e:
        print(f"❌ Genesis Test failed: {e}")
        await jaegis_master.shutdown()
        return 1


async def run_health_check():
    """Run a quick health check"""
    print("🏥 Running JAEGIS health check...")
    
    config = {
        'script': {'enable_api': False},
        'atlas': {'enable_api': False},
        'helm': {'enable_api': False},
        'mastr': {'enable_api': False},
        'ascend': {'enable_api': False},
        'cori': {'enable_htm': True, 'enable_cognitive_map': True},
        'cockpit': {'enable_api': False}
    }
    
    jaegis_master = JAEGISMaster(config)
    
    try:
        if not await jaegis_master.startup():
            print("❌ Failed to start JAEGIS ecosystem for health check")
            return 1
        
        health = await jaegis_master.health_check()
        
        print("\n📊 JAEGIS Health Report")
        print("="*50)
        print(f"Overall Status: {'✅ HEALTHY' if health['healthy'] else '❌ UNHEALTHY'}")
        print(f"Total Services: {health['ecosystem_metrics']['total_services']}")
        print(f"Healthy Services: {health['ecosystem_metrics']['healthy_services']}")
        
        print("\n🔧 Service Status:")
        for service_name, service_health in health['services'].items():
            status = "✅" if service_health.get('healthy', False) else "❌"
            print(f"   {status} {service_name.upper()}")
        
        await jaegis_master.shutdown()
        return 0 if health['healthy'] else 1
    
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="JAEGIS - Just Another Extremely General Intelligence System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_jaegis.py                    # Start in normal operation mode
  python start_jaegis.py --genesis-test     # Run the Genesis Test
  python start_jaegis.py --health-check     # Run health check only
        """
    )
    
    parser.add_argument(
        '--genesis-test',
        action='store_true',
        help='Run the Genesis Test to validate autonomous capability expansion'
    )
    
    parser.add_argument(
        '--health-check',
        action='store_true',
        help='Run a quick health check of all services'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    try:
        if args.genesis_test:
            exit_code = asyncio.run(run_genesis_test())
        elif args.health_check:
            exit_code = asyncio.run(run_health_check())
        else:
            exit_code = asyncio.run(run_normal_mode())
        
        sys.exit(exit_code)
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
