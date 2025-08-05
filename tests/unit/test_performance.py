#!/usr/bin/env python3
"""
Performance and Stress Tests for JAEGIS Session Management
==========================================================

Performance tests for session management under various load conditions.
"""

import os
import sys
import time
import tempfile
import unittest
import threading
import psutil
import gc
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.core.session_manager import JAEGISSessionManager
from common.core.session_registry import SessionRegistry


class TestSessionCreationPerformance(unittest.TestCase):
    """Test performance of session creation and destruction"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.max_sessions = 10
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_single_session_creation_speed(self):
        """Test speed of single session creation"""
        manager = JAEGISSessionManager(self.temp_dir, max_sessions=self.max_sessions)
        
        start_time = time.time()
        session_id = manager.create_session()
        creation_time = time.time() - start_time
        
        self.assertIsNotNone(session_id)
        self.assertLess(creation_time, 2.0, "Session creation should take less than 2 seconds")
        
        # Test destruction speed
        start_time = time.time()
        success = manager.destroy_session()
        destruction_time = time.time() - start_time
        
        self.assertTrue(success)
        self.assertLess(destruction_time, 1.0, "Session destruction should take less than 1 second")
    
    def test_rapid_session_creation_destruction(self):
        """Test rapid creation and destruction of sessions"""
        manager = JAEGISSessionManager(self.temp_dir, max_sessions=self.max_sessions)
        
        num_cycles = 20
        start_time = time.time()
        
        for i in range(num_cycles):
            session_id = manager.create_session()
            self.assertIsNotNone(session_id)
            
            success = manager.destroy_session()
            self.assertTrue(success)
        
        total_time = time.time() - start_time
        avg_cycle_time = total_time / num_cycles
        
        self.assertLess(avg_cycle_time, 1.0, 
                       f"Average cycle time {avg_cycle_time:.3f}s should be less than 1s")
        
        print(f"Rapid creation/destruction: {num_cycles} cycles in {total_time:.3f}s "
              f"(avg: {avg_cycle_time:.3f}s per cycle)")
    
    def test_maximum_concurrent_sessions(self):
        """Test creating maximum number of concurrent sessions"""
        managers = []
        session_ids = []
        
        start_time = time.time()
        
        try:
            # Create maximum number of sessions
            for i in range(self.max_sessions):
                manager = JAEGISSessionManager(self.temp_dir, max_sessions=self.max_sessions)
                session_id = manager.create_session()
                
                self.assertIsNotNone(session_id)
                managers.append(manager)
                session_ids.append(session_id)
            
            creation_time = time.time() - start_time
            
            # Verify all sessions are active
            registry = SessionRegistry(self.temp_dir)
            active_sessions = registry.list_sessions()
            self.assertEqual(len(active_sessions), self.max_sessions)
            
            print(f"Created {self.max_sessions} concurrent sessions in {creation_time:.3f}s")
            
            # Test cleanup time
            start_time = time.time()
            
        finally:
            # Clean up all sessions
            for manager in managers:
                try:
                    manager.destroy_session()
                except:
                    pass
            
            cleanup_time = time.time() - start_time
            print(f"Cleaned up {len(managers)} sessions in {cleanup_time:.3f}s")


class TestConcurrentAccessPerformance(unittest.TestCase):
    """Test performance under concurrent access"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.max_sessions = 5
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_concurrent_session_operations(self):
        """Test concurrent session operations"""
        num_threads = 10
        operations_per_thread = 5
        results = []
        errors = []
        
        def worker():
            try:
                for i in range(operations_per_thread):
                    manager = JAEGISSessionManager(self.temp_dir, max_sessions=self.max_sessions)
                    
                    # Try to create session
                    try:
                        session_id = manager.create_session()
                        if session_id:
                            results.append(session_id)
                            # Hold session briefly
                            time.sleep(0.1)
                            # Clean up
                            manager.destroy_session()
                    except Exception as e:
                        errors.append(e)
            except Exception as e:
                errors.append(e)
        
        start_time = time.time()
        
        # Start concurrent workers
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        print(f"Concurrent operations: {num_threads} threads × {operations_per_thread} ops "
              f"in {total_time:.3f}s")
        print(f"Successful sessions: {len(results)}, Errors: {len(errors)}")
        
        # Should have some successful operations
        self.assertGreater(len(results), 0)
        
        # Error rate should be reasonable (some expected due to session limits)
        error_rate = len(errors) / (num_threads * operations_per_thread)
        self.assertLess(error_rate, 0.8, "Error rate should be less than 80%")
    
    def test_registry_lock_contention(self):
        """Test registry performance under lock contention"""
        registry = SessionRegistry(self.temp_dir)
        num_threads = 20
        operations_per_thread = 10
        
        from common.core.session_metadata import SessionMetadata
        
        def worker(thread_id):
            for i in range(operations_per_thread):
                metadata = SessionMetadata.create_new(
                    session_id=f'test-{thread_id}-{i}',
                    allocated_ports={'script': 8080 + thread_id},
                    pid=os.getpid(),
                    resource_paths={}
                )
                
                # Register and immediately unregister
                registry.register_session(metadata)
                registry.unregister_session(metadata.session_id)
        
        start_time = time.time()
        
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        total_operations = num_threads * operations_per_thread * 2  # register + unregister
        
        print(f"Registry lock contention: {total_operations} operations in {total_time:.3f}s "
              f"({total_operations/total_time:.1f} ops/sec)")
        
        # Should complete in reasonable time
        self.assertLess(total_time, 30.0, "Registry operations should complete within 30s")


class TestMemoryUsagePerformance(unittest.TestCase):
    """Test memory usage and cleanup efficiency"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.max_sessions = 10
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_memory_usage_during_session_lifecycle(self):
        """Test memory usage during session creation and cleanup"""
        process = psutil.Process()
        
        # Get baseline memory
        gc.collect()
        baseline_memory = process.memory_info().rss
        
        managers = []
        
        try:
            # Create multiple sessions
            for i in range(self.max_sessions):
                manager = JAEGISSessionManager(self.temp_dir, max_sessions=self.max_sessions)
                session_id = manager.create_session()
                managers.append(manager)
            
            # Check memory after creation
            gc.collect()
            peak_memory = process.memory_info().rss
            memory_increase = peak_memory - baseline_memory
            
            print(f"Memory usage: baseline={baseline_memory/1024/1024:.1f}MB, "
                  f"peak={peak_memory/1024/1024:.1f}MB, "
                  f"increase={memory_increase/1024/1024:.1f}MB")
            
            # Memory increase should be reasonable
            max_expected_increase = 50 * 1024 * 1024  # 50MB
            self.assertLess(memory_increase, max_expected_increase,
                           f"Memory increase {memory_increase/1024/1024:.1f}MB should be less than 50MB")
        
        finally:
            # Clean up sessions
            for manager in managers:
                try:
                    manager.destroy_session()
                except:
                    pass
            
            # Check memory after cleanup
            gc.collect()
            final_memory = process.memory_info().rss
            
            print(f"Memory after cleanup: {final_memory/1024/1024:.1f}MB")
            
            # Memory should return close to baseline
            memory_leak = final_memory - baseline_memory
            max_acceptable_leak = 10 * 1024 * 1024  # 10MB
            self.assertLess(memory_leak, max_acceptable_leak,
                           f"Memory leak {memory_leak/1024/1024:.1f}MB should be less than 10MB")
    
    def test_memory_leak_detection(self):
        """Test for memory leaks in repeated session operations"""
        process = psutil.Process()
        
        # Perform multiple cycles of session creation/destruction
        num_cycles = 50
        memory_samples = []
        
        for cycle in range(num_cycles):
            manager = JAEGISSessionManager(self.temp_dir, max_sessions=self.max_sessions)
            session_id = manager.create_session()
            manager.destroy_session()
            
            # Sample memory every 10 cycles
            if cycle % 10 == 0:
                gc.collect()
                memory_samples.append(process.memory_info().rss)
        
        # Check for memory growth trend
        if len(memory_samples) >= 3:
            initial_memory = memory_samples[0]
            final_memory = memory_samples[-1]
            memory_growth = final_memory - initial_memory
            
            print(f"Memory leak test: {num_cycles} cycles, "
                  f"growth={memory_growth/1024/1024:.1f}MB")
            
            # Should not have significant memory growth
            max_acceptable_growth = 20 * 1024 * 1024  # 20MB
            self.assertLess(memory_growth, max_acceptable_growth,
                           f"Memory growth {memory_growth/1024/1024:.1f}MB indicates potential leak")


class TestFileSystemPerformance(unittest.TestCase):
    """Test file system operation performance"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_directory_creation_performance(self):
        """Test performance of directory creation"""
        from common.core.session_utils import create_session_directories
        
        num_sessions = 100
        start_time = time.time()
        
        created_sessions = []
        
        try:
            for i in range(num_sessions):
                session_id = f'perf-test-{i:03d}'
                directories = create_session_directories(session_id, self.temp_dir)
                created_sessions.append(session_id)
                
                # Verify directories exist
                self.assertTrue(directories['session_data'].exists())
                self.assertTrue(directories['session_logs'].exists())
                self.assertTrue(directories['session_temp'].exists())
        
        finally:
            # Clean up
            from common.core.session_utils import cleanup_session_directories
            for session_id in created_sessions:
                cleanup_session_directories(session_id, self.temp_dir)
        
        total_time = time.time() - start_time
        avg_time = total_time / num_sessions
        
        print(f"Directory creation: {num_sessions} sessions in {total_time:.3f}s "
              f"(avg: {avg_time*1000:.1f}ms per session)")
        
        # Should be fast
        self.assertLess(avg_time, 0.1, "Directory creation should take less than 100ms per session")
    
    def test_metadata_file_performance(self):
        """Test performance of metadata file operations"""
        from common.core.session_metadata import SessionMetadataManager, SessionMetadata
        
        metadata_manager = SessionMetadataManager(self.temp_dir)
        num_operations = 200
        
        # Test save performance
        start_time = time.time()
        
        for i in range(num_operations):
            metadata = SessionMetadata.create_new(
                session_id=f'perf-metadata-{i:03d}',
                allocated_ports={'script': 8080 + i},
                pid=os.getpid(),
                resource_paths={}
            )
            success = metadata_manager.save_metadata(metadata)
            self.assertTrue(success)
        
        save_time = time.time() - start_time
        
        # Test load performance
        start_time = time.time()
        
        for i in range(num_operations):
            session_id = f'perf-metadata-{i:03d}'
            metadata = metadata_manager.load_metadata(session_id)
            self.assertIsNotNone(metadata)
        
        load_time = time.time() - start_time
        
        print(f"Metadata performance: {num_operations} saves in {save_time:.3f}s "
              f"({save_time/num_operations*1000:.1f}ms each)")
        print(f"Metadata performance: {num_operations} loads in {load_time:.3f}s "
              f"({load_time/num_operations*1000:.1f}ms each)")
        
        # Should be fast
        self.assertLess(save_time/num_operations, 0.05, "Metadata save should take less than 50ms")
        self.assertLess(load_time/num_operations, 0.05, "Metadata load should take less than 50ms")


class TestStressScenarios(unittest.TestCase):
    """Stress tests for extreme scenarios"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_rapid_session_churn(self):
        """Test rapid session creation and destruction"""
        num_iterations = 100
        max_sessions = 3
        
        start_time = time.time()
        successful_operations = 0
        
        for i in range(num_iterations):
            try:
                manager = JAEGISSessionManager(self.temp_dir, max_sessions=max_sessions)
                session_id = manager.create_session()
                
                if session_id:
                    successful_operations += 1
                    # Very brief hold
                    time.sleep(0.01)
                    manager.destroy_session()
            except Exception:
                pass  # Expected due to session limits
        
        total_time = time.time() - start_time
        
        print(f"Session churn: {successful_operations}/{num_iterations} successful "
              f"in {total_time:.3f}s ({total_time/num_iterations*1000:.1f}ms per attempt)")
        
        # Should handle rapid churn without crashing
        self.assertGreater(successful_operations, 0)
        self.assertLess(total_time, 60.0, "Stress test should complete within 60s")


if __name__ == '__main__':
    print("Running JAEGIS Session Management Performance Tests")
    print("=" * 60)
    
    # Run tests with timing
    start_time = time.time()
    unittest.main(verbosity=2, exit=False)
    total_time = time.time() - start_time
    
    print(f"\nTotal test execution time: {total_time:.3f}s")
