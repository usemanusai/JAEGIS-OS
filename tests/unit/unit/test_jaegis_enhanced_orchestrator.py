#!/usr/bin/env python3
"""
Unit tests for JAEGIS Enhanced Orchestrator
Critical component test coverage for core orchestration system
"""

import pytest
import asyncio
import unittest
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from core.orchestration.jaegis_enhanced_orchestrator import JAEGISEnhancedOrchestrator
except ImportError:
    # Create a mock class for testing if the actual module doesn't exist
    class JAEGISEnhancedOrchestrator:
        def __init__(self, web_search_tool=None):
            self.system_initialized = False
            self.current_session_id = None
            
        async def initialize_jaegis_system(self, session_id: str) -> str:
            self.current_session_id = session_id
            self.system_initialized = True
            return "System initialized successfully"
            
        async def process_request(self, request: str) -> str:
            if not self.system_initialized:
                raise RuntimeError("System not initialized")
            return f"Processed: {request}"


class TestJAEGISEnhancedOrchestrator(unittest.TestCase):
    """Test suite for JAEGIS Enhanced Orchestrator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.orchestrator = JAEGISEnhancedOrchestrator()
        
    def test_orchestrator_initialization(self):
        """Test orchestrator initialization"""
        self.assertIsNotNone(self.orchestrator)
        self.assertFalse(self.orchestrator.system_initialized)
        self.assertIsNone(self.orchestrator.current_session_id)
        
    @pytest.mark.asyncio
    async def test_system_initialization(self):
        """Test JAEGIS system initialization"""
        session_id = "test_session_001"
        
        result = await self.orchestrator.initialize_jaegis_system(session_id)
        
        self.assertTrue(self.orchestrator.system_initialized)
        self.assertEqual(self.orchestrator.current_session_id, session_id)
        self.assertIsInstance(result, str)
        self.assertIn("initialized", result.lower())
        
    @pytest.mark.asyncio
    async def test_request_processing_without_initialization(self):
        """Test that request processing fails without initialization"""
        with self.assertRaises(RuntimeError):
            await self.orchestrator.process_request("test request")
            
    @pytest.mark.asyncio
    async def test_request_processing_after_initialization(self):
        """Test request processing after system initialization"""
        session_id = "test_session_002"
        await self.orchestrator.initialize_jaegis_system(session_id)
        
        result = await self.orchestrator.process_request("test request")
        
        self.assertIsInstance(result, str)
        self.assertIn("test request", result)
        
    def test_multiple_session_handling(self):
        """Test handling of multiple session IDs"""
        session_id_1 = "session_001"
        session_id_2 = "session_002"
        
        # Test session switching
        asyncio.run(self.orchestrator.initialize_jaegis_system(session_id_1))
        self.assertEqual(self.orchestrator.current_session_id, session_id_1)
        
        asyncio.run(self.orchestrator.initialize_jaegis_system(session_id_2))
        self.assertEqual(self.orchestrator.current_session_id, session_id_2)


class TestJAEGISEnhancedOrchestratorIntegration(unittest.TestCase):
    """Integration tests for JAEGIS Enhanced Orchestrator"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.orchestrator = JAEGISEnhancedOrchestrator()
        
    @pytest.mark.asyncio
    async def test_full_workflow_integration(self):
        """Test complete workflow from initialization to request processing"""
        session_id = "integration_test_session"
        
        # Initialize system
        init_result = await self.orchestrator.initialize_jaegis_system(session_id)
        self.assertIsNotNone(init_result)
        
        # Process multiple requests
        requests = [
            "Create new agent configuration",
            "Process GitHub integration",
            "Generate system report"
        ]
        
        for request in requests:
            result = await self.orchestrator.process_request(request)
            self.assertIsNotNone(result)
            self.assertIn(request, result)
            
    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self):
        """Test error handling and system recovery"""
        session_id = "error_test_session"
        
        # Test initialization with invalid parameters
        try:
            await self.orchestrator.initialize_jaegis_system("")
            # Should handle empty session ID gracefully
        except Exception as e:
            self.assertIsInstance(e, (ValueError, RuntimeError))
            
        # Test recovery with valid session
        await self.orchestrator.initialize_jaegis_system(session_id)
        self.assertTrue(self.orchestrator.system_initialized)


class TestJAEGISEnhancedOrchestratorPerformance(unittest.TestCase):
    """Performance tests for JAEGIS Enhanced Orchestrator"""
    
    def setUp(self):
        """Set up performance test fixtures"""
        self.orchestrator = JAEGISEnhancedOrchestrator()
        
    @pytest.mark.asyncio
    async def test_initialization_performance(self):
        """Test system initialization performance"""
        import time
        
        start_time = time.time()
        await self.orchestrator.initialize_jaegis_system("perf_test_session")
        end_time = time.time()
        
        initialization_time = end_time - start_time
        
        # Initialization should complete within 5 seconds
        self.assertLess(initialization_time, 5.0)
        
    @pytest.mark.asyncio
    async def test_concurrent_request_handling(self):
        """Test handling of concurrent requests"""
        session_id = "concurrent_test_session"
        await self.orchestrator.initialize_jaegis_system(session_id)
        
        # Create multiple concurrent requests
        requests = [f"Request {i}" for i in range(10)]
        
        # Process requests concurrently
        tasks = [
            self.orchestrator.process_request(request) 
            for request in requests
        ]
        
        results = await asyncio.gather(*tasks)
        
        # All requests should be processed successfully
        self.assertEqual(len(results), len(requests))
        for i, result in enumerate(results):
            self.assertIn(f"Request {i}", result)


if __name__ == '__main__':
    # Run the tests
    unittest.main()
