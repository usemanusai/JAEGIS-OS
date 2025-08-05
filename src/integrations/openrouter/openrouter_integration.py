"""
N.L.D.S. OpenRouter.ai Integration
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Integration with OpenRouter.ai for accessing 3000+ AI models and API keys
with intelligent model selection, load balancing, and cost optimization.
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta
import hashlib
import random

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# OPENROUTER STRUCTURES AND ENUMS
# ============================================================================

class ModelCategory(Enum):
    """AI model categories."""
    LANGUAGE_MODEL = "language_model"
    CHAT_MODEL = "chat_model"
    CODE_MODEL = "code_model"
    REASONING_MODEL = "reasoning_model"
    CREATIVE_MODEL = "creative_model"
    ANALYSIS_MODEL = "analysis_model"
    MULTIMODAL_MODEL = "multimodal_model"
    SPECIALIZED_MODEL = "specialized_model"


class ModelProvider(Enum):
    """AI model providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    META = "meta"
    MISTRAL = "mistral"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    TOGETHER = "together"
    OTHER = "other"


class TaskType(Enum):
    """Types of AI tasks."""
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    ANALYSIS = "analysis"
    REASONING = "reasoning"
    CREATIVE_WRITING = "creative_writing"
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"
    QUESTION_ANSWERING = "question_answering"
    CONVERSATION = "conversation"
    MULTIMODAL = "multimodal"


class LoadBalancingStrategy(Enum):
    """Load balancing strategies."""
    ROUND_ROBIN = "round_robin"
    LEAST_LOADED = "least_loaded"
    COST_OPTIMIZED = "cost_optimized"
    PERFORMANCE_OPTIMIZED = "performance_optimized"
    RANDOM = "random"
    WEIGHTED = "weighted"


@dataclass
class ModelInfo:
    """Information about an AI model."""
    model_id: str
    name: str
    provider: ModelProvider
    category: ModelCategory
    context_length: int
    cost_per_token: float
    performance_score: float = 0.0
    availability: bool = True
    capabilities: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class APIKey:
    """OpenRouter API key information."""
    key_id: str
    api_key: str
    provider: Optional[ModelProvider] = None
    rate_limit: int = 1000
    current_usage: int = 0
    last_reset: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    cost_limit: Optional[float] = None
    current_cost: float = 0.0


@dataclass
class ModelRequest:
    """Request for AI model inference."""
    request_id: str
    task_type: TaskType
    prompt: str
    model_preferences: List[str] = field(default_factory=list)
    max_tokens: int = 1000
    temperature: float = 0.7
    priority: str = "normal"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ModelResponse:
    """Response from AI model inference."""
    request_id: str
    model_used: str
    response_text: str
    tokens_used: int
    cost: float
    latency: float
    quality_score: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    completed_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# OPENROUTER INTEGRATION ENGINE
# ============================================================================

class OpenRouterIntegrationEngine:
    """
    OpenRouter.ai integration engine for accessing 3000+ AI models.
    
    Features:
    - Intelligent model selection based on task requirements
    - Load balancing across multiple API keys
    - Cost optimization and budget management
    - Rate limit management and throttling
    - Quality assessment and model performance tracking
    - Fallback and retry mechanisms
    - Real-time model availability monitoring
    - Usage analytics and optimization
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize OpenRouter integration engine."""
        self.config = config
        self.base_url = config.get('base_url', 'https://openrouter.ai/api/v1')
        self.app_name = config.get('app_name', 'JAEGIS-NLDS')
        self.app_url = config.get('app_url', 'https://github.com/usemanusai/JAEGIS-OS')
        
        # Model and API key management
        self.available_models: Dict[str, ModelInfo] = {}
        self.api_keys: Dict[str, APIKey] = {}
        self.model_performance: Dict[str, Dict[str, float]] = {}
        
        # Load balancing and optimization
        self.load_balancing_strategy = LoadBalancingStrategy(
            config.get('load_balancing_strategy', 'cost_optimized')
        )
        self.cost_budget = config.get('cost_budget', 100.0)  # USD
        self.current_cost = 0.0
        
        # Rate limiting and throttling
        self.rate_limiters: Dict[str, asyncio.Semaphore] = {}
        self.request_queue: asyncio.Queue = asyncio.Queue()
        
        # Performance tracking
        self.performance_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_cost': 0.0,
            'average_latency': 0.0,
            'model_usage': {},
            'error_rates': {}
        }
        
        # HTTP session
        self.http_session: Optional[aiohttp.ClientSession] = None
        
        # Background tasks
        self.background_tasks: Set[asyncio.Task] = set()
        
        logger.info("OpenRouter integration engine initialized")
    
    async def initialize_integration(self) -> bool:
        """Initialize OpenRouter integration."""
        try:
            # Initialize HTTP session
            self.http_session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=60),
                headers={
                    "User-Agent": "NLDS-OpenRouter/2.2.0",
                    "Content-Type": "application/json"
                }
            )
            
            # Load API keys
            await self._load_api_keys()
            
            # Load available models
            await self._load_available_models()
            
            # Start background tasks
            asyncio.create_task(self._rate_limit_monitor())
            asyncio.create_task(self._model_availability_monitor())
            
            logger.info(f"OpenRouter integration initialized with {len(self.api_keys)} API keys and {len(self.available_models)} models")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenRouter integration: {e}")
            return False
    
    async def shutdown_integration(self):
        """Shutdown OpenRouter integration."""
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
            
            logger.info("OpenRouter integration shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during OpenRouter integration shutdown: {e}")
    
    async def process_request(self, request: ModelRequest) -> Optional[ModelResponse]:
        """
        Process an AI model request with intelligent model selection.
        
        Args:
            request: ModelRequest object with task details
            
        Returns:
            ModelResponse object or None if failed
        """
        start_time = time.time()
        
        try:
            # Select optimal model
            selected_model = await self._select_optimal_model(request)
            if not selected_model:
                logger.error(f"No suitable model found for request {request.request_id}")
                return None
            
            # Select API key
            api_key = await self._select_api_key(selected_model)
            if not api_key:
                logger.error(f"No available API key for model {selected_model}")
                return None
            
            # Check rate limits
            if not await self._check_rate_limits(api_key):
                logger.warning(f"Rate limit exceeded for API key {api_key.key_id}")
                return None
            
            # Make API request
            response = await self._make_api_request(request, selected_model, api_key)
            
            if response:
                # Update performance metrics
                latency = time.time() - start_time
                await self._update_performance_metrics(selected_model, latency, True)
                
                # Update costs
                await self._update_cost_tracking(api_key, response.cost)
                
                self.performance_metrics['successful_requests'] += 1
                return response
            else:
                await self._update_performance_metrics(selected_model, 0, False)
                self.performance_metrics['failed_requests'] += 1
                return None
                
        except Exception as e:
            logger.error(f"Error processing request {request.request_id}: {e}")
            self.performance_metrics['failed_requests'] += 1
            return None
        finally:
            self.performance_metrics['total_requests'] += 1
    
    async def batch_process_requests(self, requests: List[ModelRequest]) -> List[Optional[ModelResponse]]:
        """
        Process multiple requests in parallel with load balancing.
        
        Args:
            requests: List of ModelRequest objects
            
        Returns:
            List of ModelResponse objects (or None for failed requests)
        """
        # Create semaphore for concurrent request limiting
        max_concurrent = self.config.get('max_concurrent_requests', 10)
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(request):
            async with semaphore:
                return await self.process_request(request)
        
        tasks = [process_with_semaphore(request) for request in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [
            result if not isinstance(result, Exception) else None
            for result in results
        ]
    
    async def get_model_recommendations(self, task_type: TaskType, requirements: Dict[str, Any]) -> List[str]:
        """
        Get model recommendations based on task type and requirements.
        
        Args:
            task_type: Type of AI task
            requirements: Dictionary of requirements (cost, performance, etc.)
            
        Returns:
            List of recommended model IDs
        """
        suitable_models = []
        
        for model_id, model_info in self.available_models.items():
            if not model_info.availability:
                continue
            
            # Check task compatibility
            if not await self._is_model_suitable_for_task(model_info, task_type):
                continue
            
            # Check requirements
            if not await self._meets_requirements(model_info, requirements):
                continue
            
            suitable_models.append((model_id, await self._calculate_model_score(model_info, task_type, requirements)))
        
        # Sort by score and return top recommendations
        suitable_models.sort(key=lambda x: x[1], reverse=True)
        return [model_id for model_id, _ in suitable_models[:10]]
    
    async def get_performance_analytics(self) -> Dict[str, Any]:
        """Get comprehensive performance analytics."""
        return {
            **self.performance_metrics,
            'cost_efficiency': self._calculate_cost_efficiency(),
            'model_performance_rankings': await self._get_model_performance_rankings(),
            'api_key_utilization': await self._get_api_key_utilization(),
            'availability_status': await self._get_availability_status()
        }
    
    # Private methods
    
    async def _load_api_keys(self):
        """Load API keys from configuration."""
        api_keys_config = self.config.get('api_keys', [])
        
        for key_config in api_keys_config:
            api_key = APIKey(
                key_id=key_config.get('key_id', hashlib.md5(key_config['api_key'].encode()).hexdigest()[:8]),
                api_key=key_config['api_key'],
                provider=ModelProvider(key_config.get('provider', 'other')),
                rate_limit=key_config.get('rate_limit', 1000),
                cost_limit=key_config.get('cost_limit')
            )
            
            self.api_keys[api_key.key_id] = api_key
            
            # Initialize rate limiter
            self.rate_limiters[api_key.key_id] = asyncio.Semaphore(api_key.rate_limit)
    
    async def _load_available_models(self):
        """Load available models from OpenRouter API."""
        try:
            url = f"{self.base_url}/models"
            
            # Use first available API key for model discovery
            if not self.api_keys:
                logger.warning("No API keys available for model discovery")
                return
            
            api_key = next(iter(self.api_keys.values()))
            headers = {
                "Authorization": f"Bearer {api_key.api_key}",
                "HTTP-Referer": self.app_url,
                "X-Title": self.app_name
            }
            
            async with self.http_session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for model_data in data.get('data', []):
                        model_info = ModelInfo(
                            model_id=model_data['id'],
                            name=model_data.get('name', model_data['id']),
                            provider=self._determine_provider(model_data['id']),
                            category=self._determine_category(model_data),
                            context_length=model_data.get('context_length', 4096),
                            cost_per_token=float(model_data.get('pricing', {}).get('prompt', 0)),
                            capabilities=model_data.get('capabilities', []),
                            metadata=model_data
                        )
                        
                        self.available_models[model_info.model_id] = model_info
                    
                    logger.info(f"Loaded {len(self.available_models)} models from OpenRouter")
                else:
                    logger.error(f"Failed to load models: {response.status}")
                    
        except Exception as e:
            logger.error(f"Error loading available models: {e}")
    
    async def _select_optimal_model(self, request: ModelRequest) -> Optional[str]:
        """Select optimal model for the request."""
        # Filter models based on preferences
        candidate_models = []
        
        if request.model_preferences:
            # Use preferred models if specified
            for model_id in request.model_preferences:
                if model_id in self.available_models and self.available_models[model_id].availability:
                    candidate_models.append(model_id)
        else:
            # Select based on task type and optimization strategy
            for model_id, model_info in self.available_models.items():
                if not model_info.availability:
                    continue
                
                if await self._is_model_suitable_for_task(model_info, request.task_type):
                    candidate_models.append(model_id)
        
        if not candidate_models:
            return None
        
        # Apply selection strategy
        if self.load_balancing_strategy == LoadBalancingStrategy.COST_OPTIMIZED:
            return await self._select_cost_optimized_model(candidate_models)
        elif self.load_balancing_strategy == LoadBalancingStrategy.PERFORMANCE_OPTIMIZED:
            return await self._select_performance_optimized_model(candidate_models)
        elif self.load_balancing_strategy == LoadBalancingStrategy.RANDOM:
            return random.choice(candidate_models)
        else:
            return candidate_models[0]  # Default to first available
    
    async def _select_api_key(self, model_id: str) -> Optional[APIKey]:
        """Select appropriate API key for the model."""
        available_keys = [
            key for key in self.api_keys.values()
            if key.is_active and (key.cost_limit is None or key.current_cost < key.cost_limit)
        ]
        
        if not available_keys:
            return None
        
        # Apply load balancing strategy
        if self.load_balancing_strategy == LoadBalancingStrategy.LEAST_LOADED:
            return min(available_keys, key=lambda k: k.current_usage)
        elif self.load_balancing_strategy == LoadBalancingStrategy.ROUND_ROBIN:
            # Simple round-robin based on usage count
            return min(available_keys, key=lambda k: k.current_usage)
        else:
            return available_keys[0]
    
    async def _check_rate_limits(self, api_key: APIKey) -> bool:
        """Check if API key is within rate limits."""
        # Reset usage if time window has passed
        now = datetime.utcnow()
        if (now - api_key.last_reset).total_seconds() > 3600:  # 1 hour window
            api_key.current_usage = 0
            api_key.last_reset = now
        
        # Check if under rate limit
        return api_key.current_usage < api_key.rate_limit
    
    async def _make_api_request(self, request: ModelRequest, model_id: str, api_key: APIKey) -> Optional[ModelResponse]:
        """Make API request to OpenRouter."""
        try:
            url = f"{self.base_url}/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {api_key.api_key}",
                "HTTP-Referer": self.app_url,
                "X-Title": self.app_name
            }
            
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": request.prompt}],
                "max_tokens": request.max_tokens,
                "temperature": request.temperature
            }
            
            start_time = time.time()
            
            async with self.http_session.post(url, headers=headers, json=payload) as response:
                latency = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract response data
                    choice = data['choices'][0]
                    usage = data.get('usage', {})
                    
                    # Calculate cost (simplified)
                    model_info = self.available_models[model_id]
                    tokens_used = usage.get('total_tokens', 0)
                    cost = tokens_used * model_info.cost_per_token
                    
                    # Update API key usage
                    api_key.current_usage += 1
                    
                    return ModelResponse(
                        request_id=request.request_id,
                        model_used=model_id,
                        response_text=choice['message']['content'],
                        tokens_used=tokens_used,
                        cost=cost,
                        latency=latency,
                        metadata={
                            'finish_reason': choice.get('finish_reason'),
                            'usage': usage
                        }
                    )
                else:
                    logger.error(f"API request failed: {response.status} - {await response.text()}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error making API request: {e}")
            return None
    
    async def _update_performance_metrics(self, model_id: str, latency: float, success: bool):
        """Update performance metrics for a model."""
        if model_id not in self.model_performance:
            self.model_performance[model_id] = {
                'total_requests': 0,
                'successful_requests': 0,
                'average_latency': 0.0,
                'error_rate': 0.0
            }
        
        metrics = self.model_performance[model_id]
        metrics['total_requests'] += 1
        
        if success:
            metrics['successful_requests'] += 1
            # Update average latency
            current_avg = metrics['average_latency']
            total_successful = metrics['successful_requests']
            metrics['average_latency'] = ((current_avg * (total_successful - 1)) + latency) / total_successful
        
        # Update error rate
        metrics['error_rate'] = 1 - (metrics['successful_requests'] / metrics['total_requests'])
    
    async def _update_cost_tracking(self, api_key: APIKey, cost: float):
        """Update cost tracking for API key and overall system."""
        api_key.current_cost += cost
        self.current_cost += cost
        self.performance_metrics['total_cost'] += cost
    
    async def _is_model_suitable_for_task(self, model_info: ModelInfo, task_type: TaskType) -> bool:
        """Check if model is suitable for the task type."""
        # Define task-category mappings
        task_category_map = {
            TaskType.TEXT_GENERATION: [ModelCategory.LANGUAGE_MODEL, ModelCategory.CHAT_MODEL],
            TaskType.CODE_GENERATION: [ModelCategory.CODE_MODEL, ModelCategory.LANGUAGE_MODEL],
            TaskType.ANALYSIS: [ModelCategory.ANALYSIS_MODEL, ModelCategory.REASONING_MODEL],
            TaskType.REASONING: [ModelCategory.REASONING_MODEL, ModelCategory.LANGUAGE_MODEL],
            TaskType.CREATIVE_WRITING: [ModelCategory.CREATIVE_MODEL, ModelCategory.LANGUAGE_MODEL],
            TaskType.CONVERSATION: [ModelCategory.CHAT_MODEL, ModelCategory.LANGUAGE_MODEL],
            TaskType.MULTIMODAL: [ModelCategory.MULTIMODAL_MODEL]
        }
        
        suitable_categories = task_category_map.get(task_type, [ModelCategory.LANGUAGE_MODEL])
        return model_info.category in suitable_categories
    
    async def _meets_requirements(self, model_info: ModelInfo, requirements: Dict[str, Any]) -> bool:
        """Check if model meets the specified requirements."""
        # Check cost requirements
        max_cost = requirements.get('max_cost_per_token')
        if max_cost and model_info.cost_per_token > max_cost:
            return False
        
        # Check context length requirements
        min_context = requirements.get('min_context_length')
        if min_context and model_info.context_length < min_context:
            return False
        
        # Check performance requirements
        min_performance = requirements.get('min_performance_score')
        if min_performance and model_info.performance_score < min_performance:
            return False
        
        return True
    
    async def _calculate_model_score(self, model_info: ModelInfo, task_type: TaskType, requirements: Dict[str, Any]) -> float:
        """Calculate a score for model selection."""
        score = 0.0
        
        # Base score from performance
        score += model_info.performance_score * 0.4
        
        # Cost efficiency (lower cost = higher score)
        if model_info.cost_per_token > 0:
            cost_score = 1.0 / (1.0 + model_info.cost_per_token * 1000)  # Normalize
            score += cost_score * 0.3
        
        # Task suitability
        if await self._is_model_suitable_for_task(model_info, task_type):
            score += 0.3
        
        return score
    
    async def _select_cost_optimized_model(self, candidate_models: List[str]) -> str:
        """Select the most cost-effective model."""
        return min(candidate_models, key=lambda m: self.available_models[m].cost_per_token)
    
    async def _select_performance_optimized_model(self, candidate_models: List[str]) -> str:
        """Select the highest performing model."""
        return max(candidate_models, key=lambda m: self.available_models[m].performance_score)
    
    def _determine_provider(self, model_id: str) -> ModelProvider:
        """Determine provider from model ID."""
        if 'openai' in model_id.lower() or 'gpt' in model_id.lower():
            return ModelProvider.OPENAI
        elif 'claude' in model_id.lower() or 'anthropic' in model_id.lower():
            return ModelProvider.ANTHROPIC
        elif 'gemini' in model_id.lower() or 'google' in model_id.lower():
            return ModelProvider.GOOGLE
        elif 'llama' in model_id.lower() or 'meta' in model_id.lower():
            return ModelProvider.META
        elif 'mistral' in model_id.lower():
            return ModelProvider.MISTRAL
        elif 'cohere' in model_id.lower():
            return ModelProvider.COHERE
        else:
            return ModelProvider.OTHER
    
    def _determine_category(self, model_data: Dict[str, Any]) -> ModelCategory:
        """Determine model category from model data."""
        model_id = model_data['id'].lower()
        
        if 'code' in model_id or 'codex' in model_id:
            return ModelCategory.CODE_MODEL
        elif 'chat' in model_id or 'gpt' in model_id:
            return ModelCategory.CHAT_MODEL
        elif 'vision' in model_id or 'multimodal' in model_id:
            return ModelCategory.MULTIMODAL_MODEL
        elif 'reasoning' in model_id or 'logic' in model_id:
            return ModelCategory.REASONING_MODEL
        elif 'creative' in model_id or 'story' in model_id:
            return ModelCategory.CREATIVE_MODEL
        elif 'analysis' in model_id or 'analyst' in model_id:
            return ModelCategory.ANALYSIS_MODEL
        else:
            return ModelCategory.LANGUAGE_MODEL
    
    def _calculate_cost_efficiency(self) -> float:
        """Calculate overall cost efficiency."""
        if self.performance_metrics['total_cost'] == 0:
            return 1.0
        
        return self.performance_metrics['successful_requests'] / self.performance_metrics['total_cost']
    
    async def _get_model_performance_rankings(self) -> List[Dict[str, Any]]:
        """Get model performance rankings."""
        rankings = []
        
        for model_id, metrics in self.model_performance.items():
            if metrics['total_requests'] > 0:
                rankings.append({
                    'model_id': model_id,
                    'success_rate': metrics['successful_requests'] / metrics['total_requests'],
                    'average_latency': metrics['average_latency'],
                    'total_requests': metrics['total_requests']
                })
        
        # Sort by success rate and latency
        rankings.sort(key=lambda x: (x['success_rate'], -x['average_latency']), reverse=True)
        return rankings
    
    async def _get_api_key_utilization(self) -> Dict[str, Dict[str, Any]]:
        """Get API key utilization statistics."""
        utilization = {}
        
        for key_id, api_key in self.api_keys.items():
            utilization[key_id] = {
                'usage_percentage': (api_key.current_usage / api_key.rate_limit) * 100,
                'cost_percentage': (api_key.current_cost / api_key.cost_limit * 100) if api_key.cost_limit else 0,
                'is_active': api_key.is_active,
                'current_usage': api_key.current_usage,
                'current_cost': api_key.current_cost
            }
        
        return utilization
    
    async def _get_availability_status(self) -> Dict[str, int]:
        """Get model availability status."""
        status = {
            'total_models': len(self.available_models),
            'available_models': sum(1 for m in self.available_models.values() if m.availability),
            'unavailable_models': sum(1 for m in self.available_models.values() if not m.availability)
        }
        
        return status
    
    async def _rate_limit_monitor(self):
        """Background task to monitor rate limits."""
        while True:
            try:
                # Reset rate limits every hour
                await asyncio.sleep(3600)
                
                for api_key in self.api_keys.values():
                    api_key.current_usage = 0
                    api_key.last_reset = datetime.utcnow()
                
                logger.info("Rate limits reset for all API keys")
                
            except Exception as e:
                logger.error(f"Error in rate limit monitor: {e}")
                await asyncio.sleep(60)
    
    async def _model_availability_monitor(self):
        """Background task to monitor model availability."""
        while True:
            try:
                # Check model availability every 30 minutes
                await asyncio.sleep(1800)
                
                # Reload available models
                await self._load_available_models()
                
                logger.info("Model availability updated")
                
            except Exception as e:
                logger.error(f"Error in model availability monitor: {e}")
                await asyncio.sleep(300)


# ============================================================================
# INTEGRATION FACTORY
# ============================================================================

def create_openrouter_integration(config: Dict[str, Any]) -> OpenRouterIntegrationEngine:
    """
    Factory function to create OpenRouter integration engine.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Configured OpenRouterIntegrationEngine instance
    """
    return OpenRouterIntegrationEngine(config)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def process_ai_request(prompt: str, task_type: TaskType, config: Dict[str, Any]) -> Optional[str]:
    """
    Convenience function to process a single AI request.
    
    Args:
        prompt: Input prompt for the AI model
        task_type: Type of AI task
        config: OpenRouter integration configuration
        
    Returns:
        AI response text or None if failed
    """
    engine = create_openrouter_integration(config)
    await engine.initialize_integration()
    
    try:
        request = ModelRequest(
            request_id=hashlib.md5(prompt.encode()).hexdigest()[:8],
            task_type=task_type,
            prompt=prompt
        )
        
        response = await engine.process_request(request)
        return response.response_text if response else None
        
    finally:
        await engine.shutdown_integration()


async def batch_process_ai_requests(requests: List[Tuple[str, TaskType]], config: Dict[str, Any]) -> List[Optional[str]]:
    """
    Convenience function to process multiple AI requests.
    
    Args:
        requests: List of (prompt, task_type) tuples
        config: OpenRouter integration configuration
        
    Returns:
        List of AI response texts (or None for failed requests)
    """
    engine = create_openrouter_integration(config)
    await engine.initialize_integration()
    
    try:
        model_requests = [
            ModelRequest(
                request_id=hashlib.md5(prompt.encode()).hexdigest()[:8],
                task_type=task_type,
                prompt=prompt
            )
            for prompt, task_type in requests
        ]
        
        responses = await engine.batch_process_requests(model_requests)
        return [response.response_text if response else None for response in responses]
        
    finally:
        await engine.shutdown_integration()