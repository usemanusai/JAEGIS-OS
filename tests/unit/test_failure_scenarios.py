#!/usr/bin/env python3
"""
Failure Scenario Tests for JAEGIS Session Management
===================================================

Tests for various failure scenarios including process crashes, corrupted files,
and recovery mechanisms.
"""

import os
import sys
import json
import tempfile
import unittest
import subprocess
import signal
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.core.session_manager import JAEGISSessionManager
from common.core.session_registry import SessionRegistry
from common.core.session_metadata import SessionMetadata, SessionMetadataManager


class TestProcessFailureScenarios(unittest.TestCase):
    """Test scenarios involving process failures"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.registry = SessionRegistry(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_stale_session_cleanup_dead_pid(self):
        """Test cleanup of sessions with dead PIDs"""
        # Create a session with a fake PID that doesn't exist
        fake_pid = 999999  # Very unlikely to exist
        
        metadata = SessionMetadata.create_new(
            session_id='jaegis-dead-pid-test',
            allocated_ports={'script': 8080},
            pid=fake_pid,
            resource_paths={'db': '/test/db'}
        )
        
        # Register the session
        self.registry.register_session(metadata)
        
        # Verify session is registered
        sessions = self.registry.list_sessions()
        self.assertEqual(len(sessions), 1)
        
        # Run cleanup - should remove the session with dead PID
        cleaned = self.registry.cleanup_stale_sessions()
        self.assertEqual(cleaned, 1)
        
        # Verify session was cleaned up
        sessions = self.registry.list_sessions()
        self.assertEqual(len(sessions), 0)
    
    def test_stale_session_cleanup_old_heartbeat(self):
        """Test cleanup of sessions with old heartbeats"""
        from datetime import datetime, timezone, timedelta
        
        # Create a session with old heartbeat
        old_time = datetime.now(timezone.utc) - timedelta(minutes=10)
        
        metadata = SessionMetadata.create_new(
            session_id='jaegis-old-heartbeat-test',
            allocated_ports={'script': 8080},
            pid=os.getpid(),  # Valid PID
            resource_paths={'db': '/test/db'}
        )
        
        # Manually set old heartbeat
        metadata.last_heartbeat = old_time.isoformat()
        
        # Register the session
        self.registry.register_session(metadata)
        
        # Run cleanup with short threshold
        cleaned = self.registry.cleanup_stale_sessions(stale_threshold_seconds=60)
        self.assertEqual(cleaned, 1)
    
    @patch('psutil.pid_exists')
    def test_pid_validation_edge_cases(self, mock_pid_exists):
        """Test PID validation edge cases"""
        # Test case 1: psutil.pid_exists raises exception
        mock_pid_exists.side_effect = Exception("PID check failed")
        
        metadata = SessionMetadata.create_new(
            session_id='jaegis-pid-exception-test',
            allocated_ports={'script': 8080},
            pid=12345,
            resource_paths={'db': '/test/db'}
        )
        
        self.registry.register_session(metadata)
        
        # Should clean up session when PID check fails
        cleaned = self.registry.cleanup_stale_sessions()
        self.assertEqual(cleaned, 1)
        
        # Test case 2: PID exists but process is not accessible
        mock_pid_exists.side_effect = None
        mock_pid_exists.return_value = False
        
        metadata2 = SessionMetadata.create_new(
            session_id='jaegis-pid-inaccessible-test',
            allocated_ports={'script': 8081},
            pid=12346,
            resource_paths={'db': '/test/db2'}
        )
        
        self.registry.register_session(metadata2)
        cleaned = self.registry.cleanup_stale_sessions()
        self.assertEqual(cleaned, 1)


class TestCorruptedFileScenarios(unittest.TestCase):
    """Test scenarios involving corrupted files"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.metadata_manager = SessionMetadataManager(self.temp_dir)
        self.registry = SessionRegistry(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_corrupted_registry_file(self):
        """Test handling of corrupted registry file"""
        registry_file = self.temp_dir / 'data' / 'sessions' / 'registry.json'
        registry_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write corrupted JSON
        with open(registry_file, 'w') as f:
            f.write('{"invalid": json content}')
        
        # Registry should handle corruption gracefully
        sessions = self.registry.list_sessions()
        self.assertEqual(len(sessions), 0)  # Should return empty list
        
        # Should be able to register new sessions
        metadata = SessionMetadata.create_new(
            session_id='jaegis-after-corruption-test',
            allocated_ports={'script': 8080},
            pid=os.getpid(),
            resource_paths={'db': '/test/db'}
        )
        
        success = self.registry.register_session(metadata)
        self.assertTrue(success)
    
    def test_corrupted_metadata_file(self):
        """Test handling of corrupted metadata file"""
        session_id = 'jaegis-corrupted-metadata-test'
        
        # Create corrupted metadata file
        metadata_file = self.temp_dir / 'data' / 'sessions' / f'{session_id}.json'
        metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_file, 'w') as f:
            f.write('corrupted content')
        
        # Should return None for corrupted metadata
        metadata = self.metadata_manager.load_metadata(session_id)
        self.assertIsNone(metadata)
        
        # Should be able to repair metadata
        repaired = self.metadata_manager.repair_metadata(session_id)
        self.assertIsNotNone(repaired)
        self.assertEqual(repaired.session_id, session_id)
    
    def test_partial_file_cleanup_recovery(self):
        """Test recovery from partial file cleanup"""
        session_id = 'jaegis-partial-cleanup-test'
        
        # Create session files
        session_dir = self.temp_dir / 'data' / 'sessions' / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        metadata_file = self.temp_dir / 'data' / 'sessions' / f'{session_id}.json'
        db_file = session_dir / 'jaegis.db'
        
        # Create files
        metadata = SessionMetadata.create_new(
            session_id=session_id,
            allocated_ports={'script': 8080},
            pid=os.getpid(),
            resource_paths={'db': str(db_file)}
        )
        
        self.metadata_manager.save_metadata(metadata)
        db_file.touch()
        
        # Simulate partial cleanup - remove metadata but leave directory
        metadata_file.unlink()
        
        # Session manager should handle this gracefully
        manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        
        # Should be able to create new session despite orphaned directory
        new_session_id = manager.create_session()
        self.assertIsNotNone(new_session_id)
        
        manager.destroy_session()


class TestSystemCrashRecovery(unittest.TestCase):
    """Test system crash recovery scenarios"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_recovery_after_simulated_crash(self):
        """Test recovery after simulated system crash"""
        # Create sessions before "crash"
        manager1 = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        session1_id = manager1.create_session()
        
        manager2 = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        session2_id = manager2.create_session()
        
        # Verify sessions exist
        registry = SessionRegistry(self.temp_dir)
        sessions = registry.list_sessions()
        self.assertEqual(len(sessions), 2)
        
        # Simulate crash by not cleaning up sessions properly
        # (just abandon the managers without calling destroy_session)
        del manager1
        del manager2
        
        # Create new manager after "crash"
        recovery_manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        
        # Should be able to clean up stale sessions
        cleaned = recovery_manager.cleanup_stale_sessions()
        
        # Should be able to create new session
        new_session_id = recovery_manager.create_session()
        self.assertIsNotNone(new_session_id)
        
        recovery_manager.destroy_session()
    
    def test_lock_file_recovery(self):
        """Test recovery from stale lock files"""
        registry = SessionRegistry(self.temp_dir)
        lock_file = self.temp_dir / 'data' / 'sessions' / '.registry.lock'
        
        # Create stale lock file
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        lock_file.touch()
        
        # Should still be able to operate (filelock handles stale locks)
        metadata = SessionMetadata.create_new(
            session_id='jaegis-lock-recovery-test',
            allocated_ports={'script': 8080},
            pid=os.getpid(),
            resource_paths={'db': '/test/db'}
        )
        
        success = registry.register_session(metadata)
        self.assertTrue(success)


class TestResourceExhaustionScenarios(unittest.TestCase):
    """Test resource exhaustion scenarios"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_disk_space_exhaustion(self):
        """Test handling of disk space exhaustion"""
        # This is difficult to test without actually filling up disk
        # We'll simulate by making directory read-only
        
        sessions_dir = self.temp_dir / 'data' / 'sessions'
        sessions_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Make directory read-only
            sessions_dir.chmod(0o444)
            
            # Should fail gracefully
            manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
            
            # This might fail or fall back to degraded mode
            try:
                session_id = manager.create_session()
                # If it succeeds, it should be in degraded mode
                if session_id:
                    session_info = manager.get_session_info()
                    # Check if it's degraded mode
                    self.assertTrue(session_info.get('degraded_mode', False))
            except Exception:
                # Failure is also acceptable
                pass
        
        finally:
            # Restore permissions
            try:
                sessions_dir.chmod(0o755)
            except:
                pass
    
    @patch('socket.socket')
    def test_port_exhaustion(self, mock_socket):
        """Test handling when all ports are in use"""
        # Mock socket to simulate all ports in use
        mock_socket_instance = MagicMock()
        mock_socket_instance.bind.side_effect = OSError("Address already in use")
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        
        manager = JAEGISSessionManager(self.temp_dir, max_sessions=3)
        
        # Should fail to create session due to port exhaustion
        with self.assertRaises(Exception):
            manager.create_session()


class TestConcurrencyFailures(unittest.TestCase):
    """Test concurrency-related failures"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_concurrent_session_creation_race(self):
        """Test race conditions in concurrent session creation"""
        import threading
        
        results = []
        errors = []
        
        def create_session():
            try:
                manager = JAEGISSessionManager(self.temp_dir, max_sessions=2)
                session_id = manager.create_session()
                results.append(session_id)
            except Exception as e:
                errors.append(e)
        
        # Start multiple threads trying to create sessions
        threads = []
        for i in range(5):  # More threads than max sessions
            thread = threading.Thread(target=create_session)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Should have created exactly max_sessions (2) sessions
        # and rejected the rest
        self.assertLessEqual(len(results), 2)
        self.assertGreater(len(errors), 0)  # Some should have failed
        
        # Clean up created sessions
        for session_id in results:
            if session_id:
                try:
                    manager = JAEGISSessionManager(self.temp_dir, max_sessions=2)
                    manager.destroy_session(session_id)
                except:
                    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
