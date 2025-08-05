#!/usr/bin/env python3
"""
Integration Tests for JAEGIS Session Management
===============================================

Comprehensive integration tests for multi-session scenarios, resource isolation,
and cross-component functionality.
"""

import os
import sys
import asyncio
import tempfile
import unittest
import threading
import time
import socket
from pathlib import Path
from unittest.mock import patch

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.core.session_manager import JAEGISSessionManager
from common.core.session_cli import SessionCLI
from common.core.base_launcher import BaseJAEGISLauncher
from common.core.service_discovery import JAEGISServiceDiscovery
from common.core.graceful_degradation import check_and_create_session_manager


class TestMultiSessionIntegration(unittest.TestCase):
    """Integration tests for multiple concurrent sessions"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.session_managers = []
    
    def tearDown(self):
        """Clean up test environment"""
        # Clean up all session managers
        for manager in self.session_managers:
            try:
                if manager.session_id:
                    manager.destroy_session()
            except:
                pass
        
        # Remove temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_concurrent_session_creation(self):
        """Test creating multiple concurrent sessions"""
        max_sessions = 3
        created_sessions = []
        
        # Create multiple sessions
        for i in range(max_sessions):
            manager = JAEGISSessionManager(self.temp_dir, max_sessions=max_sessions)
            session_id = manager.create_session()
            
            self.assertIsNotNone(session_id)
            self.assertTrue(session_id.startswith('jaegis-'))
            
            created_sessions.append(session_id)
            self.session_managers.append(manager)
        
        # Verify all sessions are unique
        self.assertEqual(len(set(created_sessions)), max_sessions)
        
        # Verify all sessions are registered
        registry_manager = JAEGISSessionManager(self.temp_dir, max_sessions=max_sessions)
        active_sessions = registry_manager.list_sessions()
        self.assertEqual(len(active_sessions), max_sessions)
    
    def test_port_isolation(self):
        """Test that sessions get isolated port ranges"""
        max_sessions = 3
        allocated_ports = []
        
        # Create multiple sessions and collect their ports
        for i in range(max_sessions):
            manager = JAEGISSessionManager(self.temp_dir, max_sessions=max_sessions)
            session_id = manager.create_session()
            ports = manager.get_allocated_ports()
            
            self.assertIsNotNone(ports)
            allocated_ports.append(ports)
            self.session_managers.append(manager)
        
        # Verify no port conflicts
        all_ports = []
        for ports in allocated_ports:
            for service, port in ports.items():
                if not service.startswith('reserved_'):
                    self.assertNotIn(port, all_ports, f"Port {port} allocated to multiple sessions")
                    all_ports.append(port)
        
        # Verify port ranges are correct
        for i, ports in enumerate(allocated_ports):
            expected_base = 8080 + (i * 20)
            self.assertEqual(ports['script'], expected_base)
            self.assertEqual(ports['atlas'], expected_base + 1)
            self.assertEqual(ports['cockpit'], expected_base + 10)
    
    def test_resource_isolation(self):
        """Test that sessions have isolated resources"""
        max_sessions = 2
        session_dirs = []
        
        # Create sessions and check their directories
        for i in range(max_sessions):
            manager = JAEGISSessionManager(self.temp_dir, max_sessions=max_sessions)
            session_id = manager.create_session()
            
            # Check session directories exist
            session_data_dir = self.temp_dir / 'data' / 'sessions' / session_id
            session_logs_dir = self.temp_dir / 'logs' / session_id
            session_temp_dir = self.temp_dir / 'temp' / session_id
            
            self.assertTrue(session_data_dir.exists())
            self.assertTrue(session_logs_dir.exists())
            self.assertTrue(session_temp_dir.exists())
            
            session_dirs.append({
                'data': session_data_dir,
                'logs': session_logs_dir,
                'temp': session_temp_dir
            })
            
            self.session_managers.append(manager)
        
        # Verify directories are unique
        for i in range(len(session_dirs)):
            for j in range(i + 1, len(session_dirs)):
                self.assertNotEqual(session_dirs[i]['data'], session_dirs[j]['data'])
                self.assertNotEqual(session_dirs[i]['logs'], session_dirs[j]['logs'])
                self.assertNotEqual(session_dirs[i]['temp'], session_dirs[j]['temp'])
    
    def test_configuration_isolation(self):
        """Test that sessions have isolated configurations"""
        max_sessions = 2
        
        # Create sessions with different configurations
        for i in range(max_sessions):
            manager = JAEGISSessionManager(self.temp_dir, max_sessions=max_sessions)
            session_id = manager.create_session()
            
            # Get session-specific managers
            managers = manager.get_session_managers()
            config_overlay = managers['config']
            
            if config_overlay:
                # Set session-specific configuration
                config_overlay.set_session_override(f'test_setting_{i}', f'value_{i}')
                
                # Verify configuration is set
                value = config_overlay.get_config_value(f'test_setting_{i}')
                self.assertEqual(value, f'value_{i}')
            
            self.session_managers.append(manager)
        
        # Verify configurations are isolated
        if len(self.session_managers) >= 2:
            managers1 = self.session_managers[0].get_session_managers()
            managers2 = self.session_managers[1].get_session_managers()
            
            if managers1['config'] and managers2['config']:
                # Check that session 1 can't see session 2's config
                value1 = managers1['config'].get_config_value('test_setting_1')
                value2_from_1 = managers1['config'].get_config_value('test_setting_1')
                
                self.assertEqual(value1, 'value_1')
                self.assertIsNone(managers1['config'].get_config_value('test_setting_1'))


class TestServiceDiscoveryIntegration(unittest.TestCase):
    """Integration tests for service discovery"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_service_discovery_with_session(self):
        """Test service discovery with session management"""
        # Create session
        manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        session_id = manager.create_session()
        
        try:
            # Create service discovery
            discovery = JAEGISServiceDiscovery(session_id, self.temp_dir)
            
            # Check that services are auto-registered from session config
            services = discovery.list_services()
            self.assertGreater(len(services), 0)
            
            # Verify service ports match session allocation
            allocated_ports = manager.get_allocated_ports()
            for service_info in services:
                service_name = service_info['name']
                if service_name in allocated_ports:
                    self.assertEqual(service_info['port'], allocated_ports[service_name])
        
        finally:
            manager.destroy_session()


class TestCLIIntegration(unittest.TestCase):
    """Integration tests for CLI functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.cli = SessionCLI(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_cli_session_lifecycle(self):
        """Test complete session lifecycle through CLI"""
        # Create session
        manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        session_id = manager.create_session()
        
        try:
            # List sessions
            sessions = self.cli.registry.list_sessions()
            self.assertEqual(len(sessions), 1)
            self.assertEqual(sessions[0]['session_id'], session_id)
            
            # Check session status
            session_info = self.cli.registry.get_session(session_id)
            self.assertIsNotNone(session_info)
            self.assertEqual(session_info['session_id'], session_id)
        
        finally:
            manager.destroy_session()


class TestGracefulDegradationIntegration(unittest.TestCase):
    """Integration tests for graceful degradation"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_degraded_mode_functionality(self):
        """Test functionality in degraded mode"""
        # Simulate degraded conditions by making directories read-only
        sessions_dir = self.temp_dir / 'data' / 'sessions'
        sessions_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Make directory read-only to trigger degradation
            sessions_dir.chmod(0o444)
            
            # Try to create session manager
            manager, is_degraded = check_and_create_session_manager(self.temp_dir, 3)
            
            if is_degraded:
                # Test basic functionality in degraded mode
                session_id = manager.create_session()
                self.assertIsNotNone(session_id)
                
                # Test session info retrieval
                session_info = manager.get_session_info()
                self.assertIsNotNone(session_info)
                self.assertTrue(session_info.get('degraded_mode', False))
                
                # Test session cleanup
                success = manager.destroy_session()
                self.assertTrue(success)
        
        finally:
            # Restore permissions for cleanup
            try:
                sessions_dir.chmod(0o755)
            except:
                pass


class TestLauncherIntegration(unittest.TestCase):
    """Integration tests for launcher functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_launcher_session_integration(self):
        """Test launcher with session management"""
        
        class TestLauncher(BaseJAEGISLauncher):
            async def initialize_services(self):
                return True
            
            async def start_services(self):
                return True
            
            async def stop_services(self):
                return True
            
            async def health_check(self):
                return {'status': 'healthy'}
            
            async def run_genesis_test(self):
                return {'status': 'passed'}
        
        launcher = TestLauncher("test", self.temp_dir)
        
        # Parse empty arguments
        launcher.parse_arguments([])
        
        # Initialize session management
        success = launcher.initialize_session_management()
        self.assertTrue(success)
        
        # Create session
        if launcher.use_session_management:
            success = launcher.create_session()
            self.assertTrue(success)
            
            # Check session info
            if launcher.session_id:
                config = launcher.get_session_config()
                self.assertIsInstance(config, dict)
                
                # Clean up
                launcher.cleanup_session()


async def run_async_tests():
    """Run async integration tests"""
    
    class AsyncTestLauncher(BaseJAEGISLauncher):
        def __init__(self, temp_dir):
            super().__init__("async_test", temp_dir)
        
        async def initialize_services(self):
            await asyncio.sleep(0.1)  # Simulate initialization
            return True
        
        async def start_services(self):
            await asyncio.sleep(0.1)  # Simulate startup
            return True
        
        async def stop_services(self):
            await asyncio.sleep(0.1)  # Simulate shutdown
            return True
        
        async def health_check(self):
            return {'status': 'healthy'}
        
        async def run_genesis_test(self):
            return {'status': 'passed'}
    
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        launcher = AsyncTestLauncher(temp_dir)
        launcher.parse_arguments([])
        launcher.initialize_session_management()
        
        if launcher.create_session():
            # Test async operations
            await launcher.initialize_services()
            await launcher.start_services()
            await launcher.start_session_heartbeat()
            
            # Let it run briefly
            await asyncio.sleep(1)
            
            # Clean up
            await launcher.stop_services()
            await launcher.stop_session_heartbeat()
            launcher.cleanup_session()
            
            print("✅ Async integration test passed")
        else:
            print("❌ Failed to create session for async test")
    
    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    # Run sync tests
    unittest.main(verbosity=2, exit=False)
    
    # Run async tests
    print("\n" + "="*50)
    print("Running async integration tests...")
    asyncio.run(run_async_tests())
