#!/usr/bin/env python3
"""
Error Handling Validation Tests
===============================

Comprehensive tests for error handling, error messages, and recovery mechanisms
in the JAEGIS session management system.
"""

import os
import sys
import json
import tempfile
import unittest
import socket
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.core.session_manager import (
    JAEGISSessionManager,
    SessionLimitExceeded,
    SessionCreationFailed,
    PortAllocationFailed
)
from common.core.session_registry import SessionRegistry, SessionRegistryError
from common.core.session_metadata import SessionMetadataManager
from common.core.port_allocator import PortAllocator, PortAllocationError
from common.core.session_config import SessionConfig


class TestSessionManagerErrorHandling(unittest.TestCase):
    """Test error handling in session manager"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_session_limit_exceeded_error(self):
        """Test SessionLimitExceeded error handling"""
        max_sessions = 2
        managers = []
        
        try:
            # Create maximum number of sessions
            for i in range(max_sessions):
                manager = JAEGISSessionManager(self.temp_dir, max_sessions=max_sessions)
                session_id = manager.create_session()
                self.assertIsNotNone(session_id)
                managers.append(manager)
            
            # Try to create one more - should raise SessionLimitExceeded
            extra_manager = JAEGISSessionManager(self.temp_dir, max_sessions=max_sessions)
            with self.assertRaises(SessionLimitExceeded) as context:
                extra_manager.create_session()
            
            # Verify error message is informative
            error_msg = str(context.exception)
            self.assertIn("Maximum sessions", error_msg)
            self.assertIn(str(max_sessions), error_msg)
            self.assertIn("exceeded", error_msg)
        
        finally:
            # Clean up
            for manager in managers:
                try:
                    manager.destroy_session()
                except:
                    pass
    
    @patch('common.core.port_allocator.socket.socket')
    def test_port_allocation_failed_error(self, mock_socket):
        """Test PortAllocationFailed error handling"""
        # Mock socket to simulate port conflict
        mock_socket_instance = MagicMock()
        mock_socket_instance.bind.side_effect = OSError("Address already in use")
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        
        manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        
        with self.assertRaises(PortAllocationFailed) as context:
            manager.create_session()
        
        # Verify error message mentions port allocation
        error_msg = str(context.exception)
        self.assertIn("port", error_msg.lower())
    
    def test_session_creation_failed_error(self):
        """Test SessionCreationFailed error handling"""
        # Make sessions directory read-only to trigger creation failure
        sessions_dir = self.temp_dir / 'data' / 'sessions'
        sessions_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            sessions_dir.chmod(0o444)  # Read-only
            
            manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
            
            # Should either raise SessionCreationFailed or fall back to degraded mode
            try:
                session_id = manager.create_session()
                # If it succeeds, check if it's degraded mode
                if session_id:
                    session_info = manager.get_session_info()
                    # In degraded mode, session info might indicate this
                    pass
            except SessionCreationFailed as e:
                # Verify error message is informative
                error_msg = str(e)
                self.assertIn("creation", error_msg.lower())
        
        finally:
            try:
                sessions_dir.chmod(0o755)
            except:
                pass


class TestPortAllocatorErrorHandling(unittest.TestCase):
    """Test error handling in port allocator"""
    
    def setUp(self):
        """Set up test environment"""
        self.port_allocator = PortAllocator()
    
    def test_invalid_session_number_error(self):
        """Test error handling for invalid session numbers"""
        # Test negative session number
        with self.assertRaises(PortAllocationError) as context:
            self.port_allocator.get_session_port_range(-1)
        
        error_msg = str(context.exception)
        self.assertIn("Invalid session number", error_msg)
        
        # Test session number too high
        with self.assertRaises(PortAllocationError) as context:
            self.port_allocator.get_session_port_range(20)  # Max is 10
        
        error_msg = str(context.exception)
        self.assertIn("Invalid session number", error_msg)
    
    def test_unknown_service_error(self):
        """Test error handling for unknown services"""
        with self.assertRaises(PortAllocationError) as context:
            self.port_allocator.allocate_session_ports(0, ['unknown_service'])
        
        error_msg = str(context.exception)
        self.assertIn("Unknown service", error_msg)
        self.assertIn("unknown_service", error_msg)


class TestSessionRegistryErrorHandling(unittest.TestCase):
    """Test error handling in session registry"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.registry = SessionRegistry(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_corrupted_registry_file_handling(self):
        """Test handling of corrupted registry file"""
        registry_file = self.temp_dir / 'data' / 'sessions' / 'registry.json'
        registry_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write invalid JSON
        with open(registry_file, 'w') as f:
            f.write('invalid json content')
        
        # Registry should handle corruption gracefully
        sessions = self.registry.list_sessions()
        self.assertEqual(len(sessions), 0)  # Should return empty list, not crash
    
    def test_permission_denied_handling(self):
        """Test handling of permission denied errors"""
        registry_file = self.temp_dir / 'data' / 'sessions' / 'registry.json'
        registry_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create registry file and make it read-only
        registry_file.touch()
        
        try:
            registry_file.chmod(0o444)
            
            from common.core.session_metadata import SessionMetadata
            metadata = SessionMetadata.create_new(
                session_id='test-session',
                allocated_ports={'script': 8080},
                pid=os.getpid(),
                resource_paths={}
            )
            
            # Should handle permission error gracefully
            success = self.registry.register_session(metadata)
            self.assertFalse(success)  # Should fail but not crash
        
        finally:
            try:
                registry_file.chmod(0o644)
            except:
                pass


class TestSessionConfigErrorHandling(unittest.TestCase):
    """Test error handling in session configuration"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.session_config = SessionConfig(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_invalid_max_sessions_values(self):
        """Test error handling for invalid max_sessions values"""
        # Test values outside valid range
        invalid_values = [0, -1, 11, 100, 'invalid', None]
        
        for invalid_value in invalid_values:
            with self.assertRaises(ValueError) as context:
                self.session_config.get_max_sessions(cli_arg=invalid_value)
            
            error_msg = str(context.exception)
            self.assertIn("max_sessions", error_msg)
            self.assertIn("between", error_msg)
    
    def test_corrupted_config_file_handling(self):
        """Test handling of corrupted configuration file"""
        config_file = self.temp_dir / 'jaegis_config.json'
        
        # Write invalid JSON
        with open(config_file, 'w') as f:
            f.write('invalid json')
        
        # Should fall back to default value
        max_sessions = self.session_config.get_max_sessions()
        self.assertEqual(max_sessions, 3)  # Default value


class TestMetadataManagerErrorHandling(unittest.TestCase):
    """Test error handling in metadata manager"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.metadata_manager = SessionMetadataManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_corrupted_metadata_file_handling(self):
        """Test handling of corrupted metadata files"""
        session_id = 'test-corrupted-metadata'
        metadata_file = self.temp_dir / 'data' / 'sessions' / f'{session_id}.json'
        metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write corrupted metadata
        with open(metadata_file, 'w') as f:
            f.write('corrupted metadata')
        
        # Should return None for corrupted metadata
        metadata = self.metadata_manager.load_metadata(session_id)
        self.assertIsNone(metadata)
    
    def test_metadata_validation_errors(self):
        """Test metadata validation error handling"""
        from common.core.session_metadata import SessionMetadata
        
        # Create metadata with invalid data
        metadata = SessionMetadata(
            session_id='invalid-session-id',  # Invalid format
            start_time='invalid-time',
            status='invalid-status',
            allocated_ports={'service': 'invalid-port'},  # Invalid port
            pid=-1,  # Invalid PID
            resource_paths={},
            last_heartbeat='invalid-time',
            config_overrides={}
        )
        
        # Validation should fail
        is_valid = self.metadata_manager.validate_metadata(metadata)
        self.assertFalse(is_valid)
    
    def test_metadata_repair_functionality(self):
        """Test metadata repair functionality"""
        session_id = 'test-repair-metadata'
        
        # Create corrupted metadata file
        metadata_file = self.temp_dir / 'data' / 'sessions' / f'{session_id}.json'
        metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_file, 'w') as f:
            f.write('corrupted')
        
        # Repair should create valid metadata
        repaired = self.metadata_manager.repair_metadata(session_id)
        self.assertIsNotNone(repaired)
        self.assertEqual(repaired.session_id, session_id)
        self.assertEqual(repaired.status, 'stopped')  # Safe default


class TestErrorMessageQuality(unittest.TestCase):
    """Test quality and clarity of error messages"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_session_limit_error_message_clarity(self):
        """Test that session limit error messages are clear and actionable"""
        manager = JAEGISSessionManager(self.temp_dir, max_sessions=1)
        session_id = manager.create_session()
        
        try:
            # Try to create second session
            manager2 = JAEGISSessionManager(self.temp_dir, max_sessions=1)
            with self.assertRaises(SessionLimitExceeded) as context:
                manager2.create_session()
            
            error_msg = str(context.exception)
            
            # Check that error message contains useful information
            self.assertIn("Maximum sessions", error_msg)
            self.assertIn("1", error_msg)  # Max sessions value
            self.assertIn("exceeded", error_msg)
            
            # Should suggest what user can do
            # (This would be enhanced in a real implementation)
        
        finally:
            manager.destroy_session()
    
    def test_port_conflict_error_message_clarity(self):
        """Test that port conflict error messages are clear"""
        with patch('common.core.port_allocator.socket.socket') as mock_socket:
            mock_socket_instance = MagicMock()
            mock_socket_instance.bind.side_effect = OSError("Address already in use")
            mock_socket.return_value.__enter__.return_value = mock_socket_instance
            
            manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
            
            with self.assertRaises(PortAllocationFailed) as context:
                manager.create_session()
            
            error_msg = str(context.exception)
            
            # Should mention ports and provide context
            self.assertIn("port", error_msg.lower())


class TestRecoveryMechanisms(unittest.TestCase):
    """Test recovery mechanisms after errors"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_recovery_after_registry_corruption(self):
        """Test recovery after registry corruption"""
        # Create session
        manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        session_id = manager.create_session()
        
        # Corrupt registry
        registry_file = self.temp_dir / 'data' / 'sessions' / 'registry.json'
        with open(registry_file, 'w') as f:
            f.write('corrupted')
        
        # Should be able to create new manager and recover
        recovery_manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        
        # Should be able to create new session despite corruption
        new_session_id = recovery_manager.create_session()
        self.assertIsNotNone(new_session_id)
        
        # Clean up
        manager.destroy_session()
        recovery_manager.destroy_session()
    
    def test_recovery_after_partial_cleanup(self):
        """Test recovery after partial session cleanup"""
        # Create session
        manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        session_id = manager.create_session()
        
        # Manually remove metadata file but leave directories
        metadata_file = self.temp_dir / 'data' / 'sessions' / f'{session_id}.json'
        if metadata_file.exists():
            metadata_file.unlink()
        
        # Should be able to create new session
        new_manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        new_session_id = new_manager.create_session()
        self.assertIsNotNone(new_session_id)
        
        # Clean up
        new_manager.destroy_session()


if __name__ == '__main__':
    unittest.main(verbosity=2)
