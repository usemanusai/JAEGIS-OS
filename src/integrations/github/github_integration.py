"""
N.L.D.S. GitHub Integration Interface
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Interface with GitHub integration system for dynamic resource fetching,
synchronization, and real-time access to JAEGIS repository resources.
"""

import asyncio
import aiohttp
import json
import base64
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta
import hashlib
from urllib.parse import urljoin

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# GITHUB INTEGRATION STRUCTURES AND ENUMS
# ============================================================================

class ResourceType(Enum):
    """Types of GitHub resources."""
    AGENT_CONFIG = "agent_config"
    COMMAND_TEMPLATE = "command_template"
    DOCUMENTATION = "documentation"
    CONFIGURATION = "configuration"
    SCHEMA = "schema"
    WORKFLOW = "workflow"
    SCRIPT = "script"
    DATA = "data"


class SyncStatus(Enum):
    """Synchronization status."""
    SYNCED = "synced"
    OUT_OF_SYNC = "out_of_sync"
    SYNCING = "syncing"
    ERROR = "error"
    UNKNOWN = "unknown"


class CacheStrategy(Enum):
    """Cache strategies for different resource types."""
    AGGRESSIVE = "aggressive"      # Cache everything, long TTL
    MODERATE = "moderate"          # Cache with medium TTL
    CONSERVATIVE = "conservative"  # Cache with short TTL
    NO_CACHE = "no_cache"         # No caching
    SMART = "smart"               # Intelligent caching based on resource type


@dataclass
class GitHubResource:
    """Represents a GitHub resource."""
    resource_id: str
    resource_type: ResourceType
    path: str
    content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    sha: Optional[str] = None
    size: Optional[int] = None
    cache_strategy: CacheStrategy = CacheStrategy.SMART
    sync_status: SyncStatus = SyncStatus.UNKNOWN
    last_sync: Optional[datetime] = None
    access_count: int = 0
    error_count: int = 0


@dataclass
class SyncResult:
    """Result of a synchronization operation."""
    success: bool
    resource_id: str
    sync_type: str
    timestamp: datetime
    changes_detected: bool = False
    error_message: Optional[str] = None
    performance_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchSyncRequest:
    """Request for batch synchronization."""
    resource_ids: List[str]
    sync_type: str = "full"
    priority: str = "normal"
    callback_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# GITHUB INTEGRATION ENGINE
# ============================================================================

class GitHubIntegrationEngine:
    """
    GitHub integration engine for dynamic resource fetching.
    
    Features:
    - Dynamic resource fetching from JAEGIS repository
    - Intelligent caching with multiple strategies
    - Real-time synchronization monitoring
    - Branch-aware resource access
    - Content validation and integrity checking
    - Rate limit management
    - Webhook integration for real-time updates
    - Batch operations and bulk synchronization
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize GitHub integration engine."""
        self.config = config
        self.base_url = config.get('base_url', 'https://api.github.com')
        self.repository = config.get('repository', 'usemanusai/JAEGIS-OS')
        self.branch = config.get('branch', 'main')
        self.api_token = config.get('api_token')
        
        # Resource management
        self.resource_cache: Dict[str, GitHubResource] = {}
        self.sync_queue: asyncio.Queue = asyncio.Queue()
        self.rate_limiter = asyncio.Semaphore(config.get('rate_limit', 10))
        
        # Performance tracking
        self.performance_metrics = {
            'total_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'sync_operations': 0,
            'error_count': 0,
            'average_response_time': 0.0
        }
        
        # HTTP session
        self.http_session: Optional[aiohttp.ClientSession] = None
        
        # Background tasks
        self.background_tasks: Set[asyncio.Task] = set()
        
        logger.info(f"GitHub integration engine initialized for repository: {self.repository}")
    
    async def initialize(self) -> bool:
        """Initialize the GitHub integration engine."""
        try:
            # Initialize HTTP session
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'JAEGIS-NLDS/2.2.0'
            }
            
            if self.api_token:
                headers['Authorization'] = f'token {self.api_token}'
            
            self.http_session = aiohttp.ClientSession(
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            )
            
            # Start background tasks
            sync_task = asyncio.create_task(self._background_sync_processor())
            self.background_tasks.add(sync_task)
            sync_task.add_done_callback(self.background_tasks.discard)
            
            # Validate connection
            await self._validate_connection()
            
            logger.info("GitHub integration engine initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize GitHub integration engine: {e}")
            return False
    
    async def shutdown(self):
        """Shutdown the GitHub integration engine."""
        try:
            # Cancel background tasks
            for task in self.background_tasks:
                task.cancel()
            
            # Wait for tasks to complete
            if self.background_tasks:
                await asyncio.gather(*self.background_tasks, return_exceptions=True)
            
            # Close HTTP session
            if self.http_session:
                await self.http_session.close()
            
            logger.info("GitHub integration engine shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during GitHub integration engine shutdown: {e}")
    
    async def fetch_resource(self, resource_path: str, resource_type: ResourceType = ResourceType.DATA) -> Optional[GitHubResource]:
        """
        Fetch a resource from GitHub with intelligent caching.
        
        Args:
            resource_path: Path to the resource in the repository
            resource_type: Type of resource being fetched
            
        Returns:
            GitHubResource object or None if not found
        """
        resource_id = self._generate_resource_id(resource_path)
        
        # Check cache first
        cached_resource = await self._get_cached_resource(resource_id)
        if cached_resource and await self._is_cache_valid(cached_resource):
            self.performance_metrics['cache_hits'] += 1
            cached_resource.access_count += 1
            return cached_resource
        
        self.performance_metrics['cache_misses'] += 1
        
        # Fetch from GitHub
        async with self.rate_limiter:
            start_time = asyncio.get_event_loop().time()
            
            try:
                url = f"{self.base_url}/repos/{self.repository}/contents/{resource_path}"
                params = {'ref': self.branch}
                
                async with self.http_session.get(url, params=params) as response:
                    self.performance_metrics['total_requests'] += 1
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Decode content if it's base64 encoded
                        content = None
                        if data.get('content'):
                            content = base64.b64decode(data['content']).decode('utf-8')
                        
                        # Create resource object
                        resource = GitHubResource(
                            resource_id=resource_id,
                            resource_type=resource_type,
                            path=resource_path,
                            content=content,
                            metadata={
                                'name': data.get('name'),
                                'download_url': data.get('download_url'),
                                'html_url': data.get('html_url')
                            },
                            etag=response.headers.get('ETag'),
                            sha=data.get('sha'),
                            size=data.get('size'),
                            cache_strategy=self._determine_cache_strategy(resource_type),
                            sync_status=SyncStatus.SYNCED,
                            last_sync=datetime.utcnow(),
                            access_count=1
                        )
                        
                        # Cache the resource
                        await self._cache_resource(resource)
                        
                        # Update performance metrics
                        response_time = asyncio.get_event_loop().time() - start_time
                        self._update_response_time_metric(response_time)
                        
                        return resource
                    
                    elif response.status == 404:
                        logger.warning(f"Resource not found: {resource_path}")
                        return None
                    
                    else:
                        logger.error(f"GitHub API error {response.status}: {await response.text()}")
                        self.performance_metrics['error_count'] += 1
                        return None
                        
            except Exception as e:
                logger.error(f"Error fetching resource {resource_path}: {e}")
                self.performance_metrics['error_count'] += 1
                return None
    
    async def batch_fetch_resources(self, resource_paths: List[str], resource_type: ResourceType = ResourceType.DATA) -> Dict[str, Optional[GitHubResource]]:
        """
        Fetch multiple resources in parallel.
        
        Args:
            resource_paths: List of resource paths to fetch
            resource_type: Type of resources being fetched
            
        Returns:
            Dictionary mapping resource paths to GitHubResource objects
        """
        tasks = [
            self.fetch_resource(path, resource_type)
            for path in resource_paths
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            path: result if not isinstance(result, Exception) else None
            for path, result in zip(resource_paths, results)
        }
    
    async def sync_resource(self, resource_id: str) -> SyncResult:
        """
        Synchronize a specific resource with GitHub.
        
        Args:
            resource_id: ID of the resource to synchronize
            
        Returns:
            SyncResult object with synchronization details
        """
        start_time = datetime.utcnow()
        
        try:
            cached_resource = self.resource_cache.get(resource_id)
            if not cached_resource:
                return SyncResult(
                    success=False,
                    resource_id=resource_id,
                    sync_type="sync",
                    timestamp=start_time,
                    error_message="Resource not found in cache"
                )
            
            # Fetch latest version from GitHub
            fresh_resource = await self.fetch_resource(cached_resource.path, cached_resource.resource_type)
            
            if not fresh_resource:
                return SyncResult(
                    success=False,
                    resource_id=resource_id,
                    sync_type="sync",
                    timestamp=start_time,
                    error_message="Failed to fetch resource from GitHub"
                )
            
            # Check for changes
            changes_detected = (
                cached_resource.sha != fresh_resource.sha or
                cached_resource.content != fresh_resource.content
            )
            
            if changes_detected:
                # Update cached resource
                self.resource_cache[resource_id] = fresh_resource
                logger.info(f"Resource {resource_id} updated with changes")
            
            self.performance_metrics['sync_operations'] += 1
            
            return SyncResult(
                success=True,
                resource_id=resource_id,
                sync_type="sync",
                timestamp=start_time,
                changes_detected=changes_detected,
                performance_metrics={
                    'sync_duration': (datetime.utcnow() - start_time).total_seconds()
                }
            )
            
        except Exception as e:
            logger.error(f"Error syncing resource {resource_id}: {e}")
            return SyncResult(
                success=False,
                resource_id=resource_id,
                sync_type="sync",
                timestamp=start_time,
                error_message=str(e)
            )
    
    async def batch_sync_resources(self, sync_request: BatchSyncRequest) -> List[SyncResult]:
        """
        Synchronize multiple resources in batch.
        
        Args:
            sync_request: Batch synchronization request
            
        Returns:
            List of SyncResult objects
        """
        tasks = [
            self.sync_resource(resource_id)
            for resource_id in sync_request.resource_ids
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [
            result if not isinstance(result, Exception) else SyncResult(
                success=False,
                resource_id=resource_id,
                sync_type=sync_request.sync_type,
                timestamp=datetime.utcnow(),
                error_message=str(result)
            )
            for resource_id, result in zip(sync_request.resource_ids, results)
        ]
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        return {
            **self.performance_metrics,
            'cache_size': len(self.resource_cache),
            'cache_hit_ratio': (
                self.performance_metrics['cache_hits'] / 
                max(self.performance_metrics['cache_hits'] + self.performance_metrics['cache_misses'], 1)
            ),
            'error_rate': (
                self.performance_metrics['error_count'] / 
                max(self.performance_metrics['total_requests'], 1)
            )
        }
    
    # Private methods
    
    def _generate_resource_id(self, resource_path: str) -> str:
        """Generate a unique resource ID."""
        return hashlib.md5(f"{self.repository}:{self.branch}:{resource_path}".encode()).hexdigest()
    
    async def _get_cached_resource(self, resource_id: str) -> Optional[GitHubResource]:
        """Get resource from cache."""
        return self.resource_cache.get(resource_id)
    
    async def _is_cache_valid(self, resource: GitHubResource) -> bool:
        """Check if cached resource is still valid."""
        if resource.cache_strategy == CacheStrategy.NO_CACHE:
            return False
        
        if not resource.last_sync:
            return False
        
        # Determine TTL based on cache strategy
        ttl_minutes = {
            CacheStrategy.AGGRESSIVE: 60,
            CacheStrategy.MODERATE: 30,
            CacheStrategy.CONSERVATIVE: 10,
            CacheStrategy.SMART: self._calculate_smart_ttl(resource)
        }.get(resource.cache_strategy, 30)
        
        age = datetime.utcnow() - resource.last_sync
        return age.total_seconds() < (ttl_minutes * 60)
    
    def _calculate_smart_ttl(self, resource: GitHubResource) -> int:
        """Calculate smart TTL based on resource characteristics."""
        base_ttl = 30  # minutes
        
        # Adjust based on resource type
        type_multipliers = {
            ResourceType.CONFIGURATION: 0.5,  # Config changes more frequently
            ResourceType.DOCUMENTATION: 2.0,  # Docs change less frequently
            ResourceType.SCHEMA: 3.0,         # Schemas are stable
            ResourceType.DATA: 1.0            # Default
        }
        
        multiplier = type_multipliers.get(resource.resource_type, 1.0)
        
        # Adjust based on access patterns
        if resource.access_count > 10:
            multiplier *= 1.5  # Popular resources get longer TTL
        
        return int(base_ttl * multiplier)
    
    async def _cache_resource(self, resource: GitHubResource):
        """Cache a resource."""
        self.resource_cache[resource.resource_id] = resource
        
        # Implement cache size limit
        max_cache_size = self.config.get('max_cache_size', 1000)
        if len(self.resource_cache) > max_cache_size:
            await self._evict_cache_entries()
    
    async def _evict_cache_entries(self):
        """Evict least recently used cache entries."""
        # Sort by last access time and remove oldest entries
        sorted_resources = sorted(
            self.resource_cache.items(),
            key=lambda x: x[1].last_sync or datetime.min
        )
        
        # Remove oldest 10% of entries
        evict_count = len(sorted_resources) // 10
        for resource_id, _ in sorted_resources[:evict_count]:
            del self.resource_cache[resource_id]
    
    def _determine_cache_strategy(self, resource_type: ResourceType) -> CacheStrategy:
        """Determine appropriate cache strategy for resource type."""
        strategy_map = {
            ResourceType.CONFIGURATION: CacheStrategy.CONSERVATIVE,
            ResourceType.DOCUMENTATION: CacheStrategy.MODERATE,
            ResourceType.SCHEMA: CacheStrategy.AGGRESSIVE,
            ResourceType.AGENT_CONFIG: CacheStrategy.MODERATE,
            ResourceType.WORKFLOW: CacheStrategy.MODERATE,
            ResourceType.SCRIPT: CacheStrategy.CONSERVATIVE,
            ResourceType.DATA: CacheStrategy.SMART
        }
        
        return strategy_map.get(resource_type, CacheStrategy.SMART)
    
    def _update_response_time_metric(self, response_time: float):
        """Update average response time metric."""
        current_avg = self.performance_metrics['average_response_time']
        total_requests = self.performance_metrics['total_requests']
        
        # Calculate new average
        new_avg = ((current_avg * (total_requests - 1)) + response_time) / total_requests
        self.performance_metrics['average_response_time'] = new_avg
    
    async def _validate_connection(self):
        """Validate connection to GitHub API."""
        url = f"{self.base_url}/repos/{self.repository}"
        
        async with self.http_session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to connect to GitHub API: {response.status}")
    
    async def _background_sync_processor(self):
        """Background task to process sync queue."""
        while True:
            try:
                # Wait for sync requests
                sync_request = await asyncio.wait_for(self.sync_queue.get(), timeout=60)
                
                # Process sync request
                await self.sync_resource(sync_request)
                
                # Mark task as done
                self.sync_queue.task_done()
                
            except asyncio.TimeoutError:
                # No sync requests, continue
                continue
            except Exception as e:
                logger.error(f"Error in background sync processor: {e}")
                await asyncio.sleep(5)


# ============================================================================
# INTEGRATION FACTORY
# ============================================================================

def create_github_integration(config: Dict[str, Any]) -> GitHubIntegrationEngine:
    """
    Factory function to create GitHub integration engine.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Configured GitHubIntegrationEngine instance
    """
    return GitHubIntegrationEngine(config)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def fetch_jaegis_resource(resource_path: str, config: Dict[str, Any]) -> Optional[str]:
    """
    Convenience function to fetch a JAEGIS resource.
    
    Args:
        resource_path: Path to the resource in JAEGIS repository
        config: GitHub integration configuration
        
    Returns:
        Resource content as string or None if not found
    """
    engine = create_github_integration(config)
    await engine.initialize()
    
    try:
        resource = await engine.fetch_resource(resource_path)
        return resource.content if resource else None
    finally:
        await engine.shutdown()


async def sync_jaegis_resources(resource_paths: List[str], config: Dict[str, Any]) -> Dict[str, bool]:
    """
    Convenience function to sync multiple JAEGIS resources.
    
    Args:
        resource_paths: List of resource paths to sync
        config: GitHub integration configuration
        
    Returns:
        Dictionary mapping resource paths to sync success status
    """
    engine = create_github_integration(config)
    await engine.initialize()
    
    try:
        # Fetch resources first to populate cache
        resources = await engine.batch_fetch_resources(resource_paths)
        
        # Sync resources
        resource_ids = [
            engine._generate_resource_id(path)
            for path in resource_paths
            if resources.get(path)
        ]
        
        sync_request = BatchSyncRequest(resource_ids=resource_ids)
        sync_results = await engine.batch_sync_resources(sync_request)
        
        # Map results back to paths
        result_map = {}
        for path, resource in resources.items():
            if resource:
                resource_id = engine._generate_resource_id(path)
                sync_result = next(
                    (r for r in sync_results if r.resource_id == resource_id),
                    None
                )
                result_map[path] = sync_result.success if sync_result else False
            else:
                result_map[path] = False
        
        return result_map
        
    finally:
        await engine.shutdown()