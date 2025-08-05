// CoreServiceClients.js - Integration clients for all 7 JAEGIS core services
import { authManager } from './UnifiedAuthManager';

// Base API Client
class BaseAPIClient {
  constructor(baseURL, serviceName) {
    this.baseURL = baseURL;
    this.serviceName = serviceName;
    this.healthStatus = 'unknown';
    this.lastHealthCheck = null;
  }
  
  // Make authenticated API request
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': authManager.getAuthHeader(),
        ...options.headers
      },
      ...options
    };
    
    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`${this.serviceName} API error: ${response.status} ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`${this.serviceName} request failed:`, error);
      throw error;
    }
  }
  
  // Health check
  async healthCheck() {
    try {
      const response = await this.request('/health');
      this.healthStatus = 'healthy';
      this.lastHealthCheck = new Date().toISOString();
      return response;
    } catch (error) {
      this.healthStatus = 'unhealthy';
      this.lastHealthCheck = new Date().toISOString();
      throw error;
    }
  }
  
  // Get service status
  getStatus() {
    return {
      service: this.serviceName,
      status: this.healthStatus,
      lastCheck: this.lastHealthCheck,
      url: this.baseURL
    };
  }
}

// S.C.R.I.P.T. Client (8080) - Configuration Management
class SCRIPTClient extends BaseAPIClient {
  constructor() {
    super('http://localhost:8080', 'S.C.R.I.P.T.');
  }
  
  // Get Web OS configuration
  async getWebOSConfig() {
    return await this.request('/api/config/webos');
  }
  
  // Update Web OS settings
  async updateWebOSSettings(settings) {
    return await this.request('/api/config/webos', {
      method: 'PUT',
      body: JSON.stringify(settings)
    });
  }
  
  // Get user preferences
  async getUserPreferences(userId) {
    return await this.request(`/api/config/users/${userId}/preferences`);
  }
  
  // Update user preferences
  async updateUserPreferences(userId, preferences) {
    return await this.request(`/api/config/users/${userId}/preferences`, {
      method: 'PUT',
      body: JSON.stringify(preferences)
    });
  }
  
  // Get workspace configurations
  async getWorkspaceConfigs() {
    return await this.request('/api/config/workspaces');
  }
  
  // Security analysis
  async performSecurityAnalysis() {
    return await this.request('/api/security/analyze', { method: 'POST' });
  }
}

// A.T.L.A.S. Client (8081) - Resource Synchronization
class ATLASClient extends BaseAPIClient {
  constructor() {
    super('http://localhost:8081', 'A.T.L.A.S.');
  }
  
  // Sync application data
  async syncAppData(appId) {
    return await this.request(`/api/sync/apps/${appId}`, { method: 'POST' });
  }
  
  // GitHub workspace integration
  async getGitHubWorkspace() {
    return await this.request('/api/github/workspace');
  }
  
  // Resource fetching and caching
  async fetchResource(resourceId) {
    return await this.request(`/api/resources/${resourceId}`);
  }
  
  // Data pipeline integration
  async triggerDataPipeline(pipelineId, data) {
    return await this.request(`/api/pipelines/${pipelineId}/trigger`, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }
  
  // Version control operations
  async getVersionHistory(resourceId) {
    return await this.request(`/api/resources/${resourceId}/versions`);
  }
  
  // Real-time data sync
  async enableRealTimeSync(appId) {
    return await this.request(`/api/sync/realtime/${appId}`, { method: 'POST' });
  }
}

// H.E.L.M. Client (8082) - Performance Monitoring
class HELMClient extends BaseAPIClient {
  constructor() {
    super('http://localhost:8082', 'H.E.L.M.');
  }
  
  // Get real-time metrics
  async getRealTimeMetrics() {
    return await this.request('/api/metrics/realtime');
  }
  
  // Application performance monitoring
  async getAppPerformance(appId) {
    return await this.request(`/api/performance/apps/${appId}`);
  }
  
  // System resource monitoring
  async getSystemResources() {
    return await this.request('/api/resources/system');
  }
  
  // Quality metrics tracking
  async getQualityMetrics() {
    return await this.request('/api/metrics/quality');
  }
  
  // Performance benchmarking
  async runPerformanceBenchmark(testSuite) {
    return await this.request('/api/benchmark/run', {
      method: 'POST',
      body: JSON.stringify(testSuite)
    });
  }
  
  // Set performance alerts
  async setPerformanceAlert(alertConfig) {
    return await this.request('/api/alerts/performance', {
      method: 'POST',
      body: JSON.stringify(alertConfig)
    });
  }
}

// M.A.S.T.R. Client (8083) - Tool Forging
class MASTRClient extends BaseAPIClient {
  constructor() {
    super('http://localhost:8083', 'M.A.S.T.R.');
  }
  
  // Get tool creation interface
  async getToolCreationInterface() {
    return await this.request('/api/tools/creation-interface');
  }
  
  // 4-agent squad integration
  async getSquadStatus() {
    return await this.request('/api/squad/status');
  }
  
  // Create new tool
  async createTool(toolSpec) {
    return await this.request('/api/tools/create', {
      method: 'POST',
      body: JSON.stringify(toolSpec)
    });
  }
  
  // Autonomous toolset management
  async getAutonomousToolsets() {
    return await this.request('/api/toolsets/autonomous');
  }
  
  // Tool marketplace
  async getToolMarketplace() {
    return await this.request('/api/marketplace/tools');
  }
  
  // Deploy tool
  async deployTool(toolId, deploymentConfig) {
    return await this.request(`/api/tools/${toolId}/deploy`, {
      method: 'POST',
      body: JSON.stringify(deploymentConfig)
    });
  }
}

// A.S.C.E.N.D. Client (8084) - Agent Synthesis
class ASCENDClient extends BaseAPIClient {
  constructor() {
    super('http://localhost:8084', 'A.S.C.E.N.D.');
  }
  
  // Agent creation and management
  async createAgent(agentSpec) {
    return await this.request('/api/agents/create', {
      method: 'POST',
      body: JSON.stringify(agentSpec)
    });
  }
  
  // Capability gap analysis
  async analyzeCapabilityGaps() {
    return await this.request('/api/analysis/capability-gaps');
  }
  
  // Squad architecture design
  async getSquadArchitecture() {
    return await this.request('/api/architecture/squads');
  }
  
  // Deployment management
  async getDeploymentDashboard() {
    return await this.request('/api/deployment/dashboard');
  }
  
  // Lifecycle monitoring
  async getAgentLifecycleStatus() {
    return await this.request('/api/agents/lifecycle');
  }
  
  // Agent synthesis controls
  async synthesizeAgent(synthesisConfig) {
    return await this.request('/api/synthesis/agent', {
      method: 'POST',
      body: JSON.stringify(synthesisConfig)
    });
  }
}

// C.O.R.I. Client - Cognitive Operations
class CORIClient extends BaseAPIClient {
  constructor() {
    super('http://localhost:8085', 'C.O.R.I.');
  }
  
  // HTM layer integration
  async getHTMLayerStatus() {
    return await this.request('/api/htm/status');
  }
  
  // Cognitive mapping
  async getCognitiveMap(userId) {
    return await this.request(`/api/cognitive/map/${userId}`);
  }
  
  // Prediction engine
  async getPredictions(context) {
    return await this.request('/api/predictions', {
      method: 'POST',
      body: JSON.stringify(context)
    });
  }
  
  // Intelligent task routing
  async routeTask(task) {
    return await this.request('/api/routing/task', {
      method: 'POST',
      body: JSON.stringify(task)
    });
  }
  
  // Learning loop optimization
  async optimizeLearningLoop(loopConfig) {
    return await this.request('/api/learning/optimize', {
      method: 'POST',
      body: JSON.stringify(loopConfig)
    });
  }
  
  // Proactive assistance
  async getProactiveAssistance(context) {
    return await this.request('/api/assistance/proactive', {
      method: 'POST',
      body: JSON.stringify(context)
    });
  }
}

// N.L.D.S. Client (8000) - Natural Language Processing
class NLDSClient extends BaseAPIClient {
  constructor() {
    super('http://localhost:8000', 'N.L.D.S.');
  }
  
  // Process natural language command
  async processCommand(command) {
    return await this.request('/api/nlp/process', {
      method: 'POST',
      body: JSON.stringify({ command })
    });
  }
  
  // Get command suggestions
  async getCommandSuggestions(partial) {
    return await this.request(`/api/nlp/suggestions?q=${encodeURIComponent(partial)}`);
  }
  
  // Command history
  async getCommandHistory(userId) {
    return await this.request(`/api/nlp/history/${userId}`);
  }
  
  // Confidence scoring
  async getConfidenceScore(command) {
    return await this.request('/api/nlp/confidence', {
      method: 'POST',
      body: JSON.stringify({ command })
    });
  }
  
  // Intent recognition
  async recognizeIntent(text) {
    return await this.request('/api/nlp/intent', {
      method: 'POST',
      body: JSON.stringify({ text })
    });
  }
}

// Service Manager - Manages all core services
class CoreServiceManager {
  constructor() {
    this.services = {
      script: new SCRIPTClient(),
      atlas: new ATLASClient(),
      helm: new HELMClient(),
      mastr: new MASTRClient(),
      ascend: new ASCENDClient(),
      cori: new CORIClient(),
      nlds: new NLDSClient()
    };
    
    this.healthCheckInterval = null;
    this.statusCallbacks = new Set();
  }
  
  // Initialize all services
  async initialize() {
    console.log('🔧 Initializing Core Service Manager...');
    
    // Perform initial health checks
    await this.performHealthChecks();
    
    // Start periodic health monitoring
    this.startHealthMonitoring();
    
    console.log('✅ Core Service Manager initialized');
  }
  
  // Perform health checks on all services
  async performHealthChecks() {
    const healthPromises = Object.values(this.services).map(service => 
      service.healthCheck().catch(error => ({
        service: service.serviceName,
        error: error.message
      }))
    );
    
    const results = await Promise.allSettled(healthPromises);
    this.notifyStatusCallbacks();
    
    return results;
  }
  
  // Start health monitoring
  startHealthMonitoring(interval = 30000) { // 30 seconds
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }
    
    this.healthCheckInterval = setInterval(() => {
      this.performHealthChecks();
    }, interval);
  }
  
  // Stop health monitoring
  stopHealthMonitoring() {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
      this.healthCheckInterval = null;
    }
  }
  
  // Get service by name
  getService(serviceName) {
    return this.services[serviceName.toLowerCase()];
  }
  
  // Get all service statuses
  getAllStatuses() {
    return Object.values(this.services).map(service => service.getStatus());
  }
  
  // Subscribe to status updates
  onStatusUpdate(callback) {
    this.statusCallbacks.add(callback);
    return () => this.statusCallbacks.delete(callback);
  }
  
  // Notify status callbacks
  notifyStatusCallbacks() {
    const statuses = this.getAllStatuses();
    this.statusCallbacks.forEach(callback => callback(statuses));
  }
}

// Global service manager instance
export const coreServiceManager = new CoreServiceManager();
export { SCRIPTClient, ATLASClient, HELMClient, MASTRClient, ASCENDClient, CORIClient, NLDSClient };
export default CoreServiceManager;
