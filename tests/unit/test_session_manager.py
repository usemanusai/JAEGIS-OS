#!/usr/bin/env python3
"""
Session Manager Tests
====================

Comprehensive tests for the JAEGIS session management system.
"""

import os
import json
import tempfile
import unittest
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the project root to the path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.core.session_manager import (
    JAEGISSessionManager,
    SessionLimitExceeded,
    SessionCreationFailed,
    PortAllocationFailed
)
from common.core.session_registry import SessionRegistry
from common.core.port_allocator import PortAllocator
from common.core.session_metadata import SessionMetadata
from common.core.session_config import SessionConfig


class TestSessionManager(unittest.TestCase):
    """Test cases for JAEGISSessionManager"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.session_manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
    
    def tearDown(self):
        """Clean up test environment"""
        # Clean up any created sessions
        if self.session_manager.session_id:
            self.session_manager.destroy_session()
        
        # Remove temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_session_creation(self):
        """Test basic session creation"""
        session_id = self.session_manager.create_session()
        
        self.assertIsNotNone(session_id)
        self.assertTrue(session_id.startswith('jaegis-'))
        self.assertEqual(self.session_manager.session_id, session_id)
        
        # Check that directories were created
        session_dir = self.temp_dir / 'data' / 'sessions' / session_id
        self.assertTrue(session_dir.exists())
        
        log_dir = self.temp_dir / 'logs' / session_id
        self.assertTrue(log_dir.exists())
        
        temp_dir = self.temp_dir / 'temp' / session_id
        self.assertTrue(temp_dir.exists())
    
    def test_session_metadata(self):
        """Test session metadata creation and storage"""
        session_id = self.session_manager.create_session()
        
        # Check metadata file exists
        metadata_file = self.temp_dir / 'data' / 'sessions' / f'{session_id}.json'
        self.assertTrue(metadata_file.exists())
        
        # Load and validate metadata
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        required_fields = [
            'session_id', 'start_time', 'status', 'allocated_ports',
            'pid', 'resource_paths', 'last_heartbeat', 'config_overrides'
        ]
        
        for field in required_fields:
            self.assertIn(field, metadata)
        
        self.assertEqual(metadata['session_id'], session_id)
        self.assertEqual(metadata['status'], 'starting')
    
    def test_port_allocation(self):
        """Test port allocation for sessions"""
        session_id = self.session_manager.create_session()
        
        ports = self.session_manager.get_allocated_ports()
        self.assertIsNotNone(ports)
        
        # Check that expected services have ports
        expected_services = ['script', 'atlas', 'helm', 'mastr', 'ascend', 'cori', 'cockpit']
        for service in expected_services:
            self.assertIn(service, ports)
            self.assertIsInstance(ports[service], int)
            self.assertGreaterEqual(ports[service], 8080)
            self.assertLessEqual(ports[service], 8090)
    
    def test_session_limit(self):
        """Test session limit enforcement"""
        # Create maximum number of sessions
        session_ids = []
        for i in range(3):  # max_sessions = 3
            session_id = self.session_manager.create_session()
            session_ids.append(session_id)
            
            # Create a new manager for each session to simulate multiple instances
            if i < 2:  # Don't create new manager for last iteration
                self.session_manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        
        # Try to create one more session - should fail
        new_manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        with self.assertRaises(SessionLimitExceeded):
            new_manager.create_session()
    
    def test_session_cleanup(self):
        """Test session cleanup"""
        session_id = self.session_manager.create_session()
        
        # Verify session exists
        session_info = self.session_manager.get_session_info()
        self.assertIsNotNone(session_info)
        
        # Clean up session
        success = self.session_manager.destroy_session()
        self.assertTrue(success)
        
        # Verify session is cleaned up
        self.assertIsNone(self.session_manager.session_id)
        
        # Check that directories are cleaned up
        session_dir = self.temp_dir / 'data' / 'sessions' / session_id
        self.assertFalse(session_dir.exists())
    
    def test_heartbeat_update(self):
        """Test heartbeat mechanism"""
        session_id = self.session_manager.create_session()
        
        # Get initial heartbeat
        initial_info = self.session_manager.get_session_info()
        initial_heartbeat = initial_info['last_heartbeat']
        
        # Update heartbeat
        import time
        time.sleep(0.1)  # Small delay to ensure different timestamp
        success = self.session_manager.update_heartbeat()
        self.assertTrue(success)
        
        # Check that heartbeat was updated
        updated_info = self.session_manager.get_session_info()
        updated_heartbeat = updated_info['last_heartbeat']
        
        self.assertNotEqual(initial_heartbeat, updated_heartbeat)
    
    def test_status_update(self):
        """Test session status updates"""
        session_id = self.session_manager.create_session()
        
        # Update status
        success = self.session_manager.update_session_status('running')
        self.assertTrue(success)
        
        # Verify status was updated
        session_info = self.session_manager.get_session_info()
        self.assertEqual(session_info['status'], 'running')
    
    @patch('common.core.port_allocator.socket.socket')
    def test_port_conflict_detection(self, mock_socket):
        """Test port conflict detection"""
        # Mock socket to simulate port in use
        mock_socket_instance = MagicMock()
        mock_socket_instance.bind.side_effect = OSError("Port in use")
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        
        # Should raise PortAllocationFailed
        with self.assertRaises(PortAllocationFailed):
            self.session_manager.create_session()


class TestPortAllocator(unittest.TestCase):
    """Test cases for PortAllocator"""
    
    def setUp(self):
        """Set up test environment"""
        self.port_allocator = PortAllocator()
    
    def test_port_range_calculation(self):
        """Test port range calculation for different sessions"""
        # Session 0: 8080-8099
        range_0 = self.port_allocator.get_session_port_range(0)
        self.assertEqual(range_0.start_port, 8080)
        self.assertEqual(range_0.end_port, 8099)
        
        # Session 1: 8100-8119
        range_1 = self.port_allocator.get_session_port_range(1)
        self.assertEqual(range_1.start_port, 8100)
        self.assertEqual(range_1.end_port, 8119)
        
        # Session 2: 8120-8139
        range_2 = self.port_allocator.get_session_port_range(2)
        self.assertEqual(range_2.start_port, 8120)
        self.assertEqual(range_2.end_port, 8139)
    
    def test_service_port_allocation(self):
        """Test service port allocation"""
        ports = self.port_allocator.allocate_session_ports(0)
        
        # Check expected services
        expected_services = ['script', 'atlas', 'helm', 'mastr', 'ascend', 'cori', 'cockpit']
        for service in expected_services:
            self.assertIn(service, ports)
        
        # Check port values
        self.assertEqual(ports['script'], 8080)  # Base + 0
        self.assertEqual(ports['atlas'], 8081)   # Base + 1
        self.assertEqual(ports['cockpit'], 8090) # Base + 10
    
    def test_port_validation(self):
        """Test port allocation validation"""
        ports = self.port_allocator.allocate_session_ports(0)
        
        # Should be valid
        is_valid = self.port_allocator.validate_port_allocation(0, ports)
        self.assertTrue(is_valid)
        
        # Modify ports to make invalid
        invalid_ports = ports.copy()
        invalid_ports['script'] = 9999  # Wrong port
        
        is_valid = self.port_allocator.validate_port_allocation(0, invalid_ports)
        self.assertFalse(is_valid)


class TestSessionRegistry(unittest.TestCase):
    """Test cases for SessionRegistry"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.registry = SessionRegistry(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_session_registration(self):
        """Test session registration and retrieval"""
        # Create test metadata
        metadata = SessionMetadata.create_new(
            session_id='jaegis-test-123',
            allocated_ports={'script': 8080, 'atlas': 8081},
            pid=12345,
            resource_paths={'db': '/test/db', 'logs': '/test/logs'}
        )
        
        # Register session
        success = self.registry.register_session(metadata)
        self.assertTrue(success)
        
        # Retrieve session
        retrieved = self.registry.get_session('jaegis-test-123')
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['session_id'], 'jaegis-test-123')
        self.assertEqual(retrieved['pid'], 12345)
    
    def test_session_update(self):
        """Test session updates"""
        # Register a session first
        metadata = SessionMetadata.create_new(
            session_id='jaegis-test-456',
            allocated_ports={'script': 8080},
            pid=12345,
            resource_paths={}
        )
        self.registry.register_session(metadata)
        
        # Update session
        success = self.registry.update_session('jaegis-test-456', {'status': 'running'})
        self.assertTrue(success)
        
        # Verify update
        retrieved = self.registry.get_session('jaegis-test-456')
        self.assertEqual(retrieved['status'], 'running')
    
    def test_session_unregistration(self):
        """Test session unregistration"""
        # Register a session first
        metadata = SessionMetadata.create_new(
            session_id='jaegis-test-789',
            allocated_ports={'script': 8080},
            pid=12345,
            resource_paths={}
        )
        self.registry.register_session(metadata)
        
        # Unregister session
        success = self.registry.unregister_session('jaegis-test-789')
        self.assertTrue(success)
        
        # Verify session is gone
        retrieved = self.registry.get_session('jaegis-test-789')
        self.assertIsNone(retrieved)


class TestSessionConfig(unittest.TestCase):
    """Test cases for SessionConfig"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.session_config = SessionConfig(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_default_max_sessions(self):
        """Test default max sessions value"""
        max_sessions = self.session_config.get_max_sessions()
        self.assertEqual(max_sessions, 3)  # Default value
    
    def test_cli_override(self):
        """Test CLI argument override"""
        max_sessions = self.session_config.get_max_sessions(cli_arg=5)
        self.assertEqual(max_sessions, 5)
    
    def test_environment_override(self):
        """Test environment variable override"""
        with patch.dict(os.environ, {'JAEGIS_MAX_SESSIONS': '7'}):
            max_sessions = self.session_config.get_max_sessions()
            self.assertEqual(max_sessions, 7)
    
    def test_config_file_override(self):
        """Test configuration file override"""
        # Create config file
        config_file = self.temp_dir / 'jaegis_config.json'
        config_data = {'max_concurrent_sessions': 6}
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        max_sessions = self.session_config.get_max_sessions()
        self.assertEqual(max_sessions, 6)
    
    def test_validation(self):
        """Test max sessions validation"""
        # Valid values
        for valid_value in [1, 5, 10]:
            max_sessions = self.session_config.get_max_sessions(cli_arg=valid_value)
            self.assertEqual(max_sessions, valid_value)
        
        # Invalid values
        for invalid_value in [0, 11, -1]:
            with self.assertRaises(ValueError):
                self.session_config.get_max_sessions(cli_arg=invalid_value)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
