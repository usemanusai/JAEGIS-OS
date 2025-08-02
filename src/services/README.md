# JAEGIS Core Services

**The 7 foundational services that power the JAEGIS-OS ecosystem**

The JAEGIS-OS architecture is built around 7 core services that work together to provide a comprehensive AI-powered operating system. Each service has a specific role and operates on dedicated ports, forming a distributed microservices architecture.

## 🏗️ Service Architecture

```mermaid
graph TB
    subgraph "Core Services Layer"
        NLDS[N.L.D.S.<br/>Port 8000<br/>Natural Language Processing]
        SCRIPT[S.C.R.I.P.T.<br/>Port 8080<br/>Configuration Management]
        ATLAS[A.T.L.A.S.<br/>Port 8081<br/>Resource Synchronization]
        HELM[H.E.L.M.<br/>Port 8082<br/>Performance Monitoring]
        MASTR[M.A.S.T.R.<br/>Port 8083<br/>Tool Forging]
        ASCEND[A.S.C.E.N.D.<br/>Port 8084<br/>Agent Synthesis]
        CORI[C.O.R.I.<br/>Port 8085<br/>Cognitive Operations]
    end
    
    subgraph "Web OS Desktop"
        WEBOS[Web OS Desktop<br/>Port 3000<br/>React 18 Frontend]
    end
    
    subgraph "Infrastructure"
        PG[(PostgreSQL<br/>Multi-Database)]
        REDIS[(Redis<br/>Caching)]
        NGINX[NGINX<br/>Load Balancer]
    end
    
    WEBOS --> NLDS
    WEBOS --> SCRIPT
    WEBOS --> ATLAS
    WEBOS --> HELM
    WEBOS --> MASTR
    WEBOS --> ASCEND
    WEBOS --> CORI
    
    NLDS --> PG
    SCRIPT --> PG
    ATLAS --> PG
    HELM --> PG
    MASTR --> PG
    ASCEND --> PG
    CORI --> PG
    
    NLDS --> REDIS
    SCRIPT --> REDIS
    ATLAS --> REDIS
    HELM --> REDIS
    MASTR --> REDIS
    ASCEND --> REDIS
    CORI --> REDIS
    
    NGINX --> WEBOS
    NGINX --> NLDS
    NGINX --> SCRIPT
    NGINX --> ATLAS
    NGINX --> HELM
    NGINX --> MASTR
    NGINX --> ASCEND
    NGINX --> CORI
```

## 🔧 Service Overview

| Service | Port | Purpose | Status | Load | Tier |
|---------|------|---------|--------|------|------|
| **N.L.D.S.** | 8000 | Natural Language Processing & Command Center | 🟢 Active | 45% | 0 |
| **S.C.R.I.P.T.** | 8080 | Configuration Management & System Setup | 🟢 Active | 32% | 1 |
| **A.T.L.A.S.** | 8081 | Resource Synchronization & Data Management | 🟢 Active | 28% | 1 |
| **H.E.L.M.** | 8082 | Performance Monitoring & Health Management | 🟢 Active | 41% | 1 |
| **M.A.S.T.R.** | 8083 | Tool Forging & Development Utilities | 🟢 Active | 35% | 1 |
| **A.S.C.E.N.D.** | 8084 | Agent Synthesis & Deployment | 🟢 Active | 39% | 1 |
| **C.O.R.I.** | 8085 | Cognitive Operations & AI Processing | 🟢 Active | 22% | 1 |

## 📁 Service Structure

```
src/services/
├── nlds/                        # N.L.D.S. - Natural Language Processing
│   ├── api/                    # API endpoints and routes
│   ├── nlp/                    # NLP processing engines
│   ├── cognitive/              # Cognitive processing
│   ├── confidence/             # Confidence scoring
│   ├── integration/            # Service integrations
│   ├── processing/             # Command processing
│   ├── translation/            # Language translation
│   └── README.md               # Service documentation
├── script/                      # S.C.R.I.P.T. - Configuration Management
│   ├── config/                 # Configuration management
│   ├── setup/                  # System setup utilities
│   ├── validation/             # Configuration validation
│   ├── templates/              # Configuration templates
│   └── README.md               # Service documentation
├── atlas/                       # A.T.L.A.S. - Resource Synchronization
│   ├── sync/                   # Data synchronization
│   ├── resources/              # Resource management
│   ├── github/                 # GitHub integration
│   ├── pipelines/              # Data pipelines
│   └── README.md               # Service documentation
├── helm/                        # H.E.L.M. - Performance Monitoring
│   ├── monitoring/             # System monitoring
│   ├── metrics/                # Performance metrics
│   ├── health/                 # Health checks
│   ├── alerts/                 # Alert management
│   └── README.md               # Service documentation
├── mastr/                       # M.A.S.T.R. - Tool Forging
│   ├── forge/                  # Tool creation
│   ├── templates/              # Tool templates
│   ├── deployment/             # Tool deployment
│   ├── management/             # Tool management
│   └── README.md               # Service documentation
├── ascend/                      # A.S.C.E.N.D. - Agent Synthesis
│   ├── synthesis/              # Agent creation
│   ├── deployment/             # Agent deployment
│   ├── coordination/           # Agent coordination
│   ├── templates/              # Agent templates
│   └── README.md               # Service documentation
├── cori/                        # C.O.R.I. - Cognitive Operations
│   ├── cognitive/              # Cognitive processing
│   ├── ai/                     # AI operations
│   ├── learning/               # Machine learning
│   ├── reasoning/              # Reasoning engines
│   └── README.md               # Service documentation
└── shared/                      # Shared service utilities
    ├── BaseService.js          # Base service class
    ├── ServiceRegistry.js      # Service discovery
    ├── HealthMonitor.js        # Health monitoring
    └── APIClient.js            # API client utilities
```

## 🧠 N.L.D.S. - Natural Language Processing (Port 8000)

**Tier 0 Command Center - The brain of the JAEGIS ecosystem**

N.L.D.S. (Natural Language Data System) serves as the primary command center and natural language processing engine for the entire JAEGIS-OS ecosystem.

### Key Features
- **Natural Language Processing**: Advanced NLP for command interpretation
- **Command Coordination**: Central command routing and processing
- **Intent Recognition**: Intelligent intent detection and confidence scoring
- **Multi-language Support**: Translation and localization capabilities
- **Cognitive Processing**: Advanced reasoning and decision making

### API Endpoints
```javascript
// Process natural language commands
POST /api/nlp/process
{
  "command": "open file explorer",
  "context": "desktop_environment"
}

// Get command suggestions
GET /api/nlp/suggestions?q=open

// Recognize intent
POST /api/nlp/intent
{
  "text": "show me system status"
}

// Get confidence score
POST /api/nlp/confidence
{
  "command": "launch application",
  "context": "user_request"
}
```

### Integration Example
```javascript
const NLDSClient = require('./nlds/NLDSClient');

const nlds = new NLDSClient('http://localhost:8000');

const result = await nlds.processCommand('open terminal');
// Returns: { intent: 'launch_app', confidence: 0.95, app: 'terminal' }
```

## ⚙️ S.C.R.I.P.T. - Configuration Management (Port 8080)

**System Configuration, Resource Integration, and Project Templates**

S.C.R.I.P.T. manages all system configuration, setup procedures, and project templates across the JAEGIS ecosystem.

### Key Features
- **Configuration Management**: Centralized config for all services
- **System Setup**: Automated installation and configuration
- **Template Management**: Project and service templates
- **Environment Configuration**: Multi-environment support
- **Validation**: Configuration validation and testing

### API Endpoints
```javascript
// Get system configuration
GET /api/config/system

// Update service configuration
PUT /api/config/services/{serviceName}
{
  "port": 8000,
  "database": "postgresql://...",
  "redis": "redis://..."
}

// Validate configuration
POST /api/config/validate
{
  "config": { ... }
}

// Get templates
GET /api/templates/{templateType}
```

## 🗄️ A.T.L.A.S. - Resource Synchronization (Port 8081)

**Advanced Technology for Logistics and Synchronization**

A.T.L.A.S. handles all resource synchronization, data management, and external integrations.

### Key Features
- **Data Synchronization**: Real-time data sync across services
- **Resource Management**: Centralized resource allocation
- **GitHub Integration**: Repository and workspace sync
- **Data Pipelines**: Automated data processing workflows
- **Backup Management**: Data backup and recovery

### API Endpoints
```javascript
// Sync application data
POST /api/sync/apps/{appId}

// Get GitHub workspace
GET /api/github/workspace

// Trigger data pipeline
POST /api/pipelines/{pipelineId}/trigger
{
  "data": { ... }
}

// Fetch resource
GET /api/resources/{resourceId}
```

## 📊 H.E.L.M. - Performance Monitoring (Port 8082)

**Health, Efficiency, and Lifecycle Management**

H.E.L.M. provides comprehensive monitoring, health checks, and performance management for the entire ecosystem.

### Key Features
- **Real-time Monitoring**: Live system metrics and performance data
- **Health Checks**: Automated health monitoring for all services
- **Performance Analytics**: Detailed performance analysis and reporting
- **Alert Management**: Intelligent alerting and notification system
- **Resource Tracking**: CPU, memory, network, and disk monitoring

### API Endpoints
```javascript
// Get real-time metrics
GET /api/metrics/realtime

// Get system resources
GET /api/resources/system

// Get application performance
GET /api/performance/apps/{appId}

// Run performance benchmark
POST /api/benchmark/run
{
  "testSuite": "comprehensive",
  "duration": 300
}
```

### Monitoring Dashboard
```javascript
const HELMClient = require('./helm/HELMClient');

const helm = new HELMClient('http://localhost:8082');

// Get real-time system metrics
const metrics = await helm.getRealTimeMetrics();
console.log(`CPU: ${metrics.cpu.usage}%`);
console.log(`Memory: ${metrics.memory.used}MB/${metrics.memory.total}MB`);
```

## 🔨 M.A.S.T.R. - Tool Forging (Port 8083)

**Modular Agent System for Tool Refinement**

M.A.S.T.R. handles tool creation, management, and deployment across the JAEGIS ecosystem.

### Key Features
- **Tool Forging**: Create and customize development tools
- **Template System**: Pre-built tool templates and configurations
- **Deployment Management**: Tool deployment and distribution
- **Version Control**: Tool versioning and update management
- **Integration**: Seamless tool integration with other services

### API Endpoints
```javascript
// Create new tool
POST /api/tools/create
{
  "name": "Custom Analyzer",
  "type": "analysis",
  "template": "analyzer_template"
}

// Deploy tool
POST /api/tools/{toolId}/deploy
{
  "environment": "production",
  "config": { ... }
}

// Get tool templates
GET /api/templates/tools

// Manage tool versions
GET /api/tools/{toolId}/versions
```

## 🚀 A.S.C.E.N.D. - Agent Synthesis (Port 8084)

**Adaptive System for Cognitive Enhancement and Neural Development**

A.S.C.E.N.D. manages the creation, deployment, and coordination of the 7-tier agent hierarchy.

### Key Features
- **Agent Synthesis**: Create and configure intelligent agents
- **Deployment Management**: Deploy agents across the 7-tier hierarchy
- **Coordination**: Multi-agent coordination and communication
- **Learning**: Agent learning and adaptation capabilities
- **Performance Optimization**: Agent performance tuning

### API Endpoints
```javascript
// Create new agent
POST /api/agents/create
{
  "name": "Research Agent",
  "type": "research",
  "tier": 6,
  "capabilities": ["web-search", "data-analysis"]
}

// Deploy agent
POST /api/agents/{agentId}/deploy
{
  "tier": 6,
  "squad": "research_squad"
}

// Get agent status
GET /api/agents/{agentId}/status

// Coordinate agents
POST /api/coordination/squads/{squadId}/task
{
  "task": "research_topic",
  "agents": ["agent1", "agent2"]
}
```

## 🧠 C.O.R.I. - Cognitive Operations (Port 8085)

**Cognitive Operations and Reasoning Intelligence**

C.O.R.I. provides advanced AI processing, machine learning, and cognitive operations for the entire ecosystem.

### Key Features
- **Cognitive Processing**: Advanced reasoning and decision making
- **AI Operations**: Machine learning model management
- **Learning Systems**: Adaptive learning and improvement
- **Reasoning Engines**: Logic and inference systems
- **Knowledge Management**: Knowledge base and expert systems

### API Endpoints
```javascript
// Process cognitive task
POST /api/cognitive/process
{
  "task": "analyze_data",
  "data": { ... },
  "context": "research"
}

// Train model
POST /api/ai/models/train
{
  "modelType": "classification",
  "data": "training_dataset",
  "parameters": { ... }
}

// Reasoning query
POST /api/reasoning/query
{
  "query": "What is the best approach for this problem?",
  "context": { ... }
}
```

## 🔄 Service Communication

### Inter-Service Communication

```javascript
const ServiceRegistry = require('./shared/ServiceRegistry');

class ServiceCommunicator {
  constructor() {
    this.registry = new ServiceRegistry();
  }

  async callService(serviceName, endpoint, data) {
    const service = await this.registry.discover(serviceName);
    const response = await fetch(`${service.url}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }
}

// Example: NLDS calling HELM for metrics
const communicator = new ServiceCommunicator();
const metrics = await communicator.callService('helm', '/api/metrics/realtime', {});
```

### Event-Driven Architecture

```javascript
const EventBus = require('./shared/EventBus');

class ServiceEventHandler {
  constructor(serviceName) {
    this.serviceName = serviceName;
    this.eventBus = new EventBus();
    this.setupEventHandlers();
  }

  setupEventHandlers() {
    this.eventBus.on('service.health.check', this.handleHealthCheck.bind(this));
    this.eventBus.on('agent.task.completed', this.handleTaskCompleted.bind(this));
  }

  async handleHealthCheck(event) {
    const health = await this.performHealthCheck();
    this.eventBus.emit('service.health.response', {
      service: this.serviceName,
      health
    });
  }
}
```

## 🛡️ Security and Authentication

### Service Authentication

```javascript
const jwt = require('jsonwebtoken');

class ServiceAuth {
  static generateServiceToken(serviceName) {
    return jwt.sign(
      { service: serviceName, type: 'service' },
      process.env.SERVICE_SECRET,
      { expiresIn: '1h' }
    );
  }

  static verifyServiceToken(token) {
    return jwt.verify(token, process.env.SERVICE_SECRET);
  }
}

// Middleware for service authentication
const authenticateService = (req, res, next) => {
  const token = req.headers['x-service-token'];
  try {
    const decoded = ServiceAuth.verifyServiceToken(token);
    req.service = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid service token' });
  }
};
```

## 📊 Health Monitoring

### Service Health Checks

```javascript
const HealthMonitor = require('./shared/HealthMonitor');

class ServiceHealth extends HealthMonitor {
  constructor(serviceName, port) {
    super(serviceName);
    this.port = port;
  }

  async performHealthCheck() {
    const checks = {
      database: await this.checkDatabase(),
      redis: await this.checkRedis(),
      memory: this.checkMemory(),
      cpu: this.checkCPU(),
      dependencies: await this.checkDependencies()
    };

    const isHealthy = Object.values(checks).every(check => check.status === 'healthy');

    return {
      service: this.serviceName,
      status: isHealthy ? 'healthy' : 'unhealthy',
      port: this.port,
      checks,
      timestamp: new Date().toISOString()
    };
  }
}
```

## 🚀 Deployment

### Docker Configuration

```yaml
# docker-compose.yml for all services
version: '3.8'

services:
  nlds:
    build: ./nlds
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://nlds_user:password@postgres:5432/nlds
      - REDIS_URL=redis://redis:6379/0

  script:
    build: ./script
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://script_user:password@postgres:5432/script
      - REDIS_URL=redis://redis:6379/1

  atlas:
    build: ./atlas
    ports:
      - "8081:8081"
    environment:
      - DATABASE_URL=postgresql://atlas_user:password@postgres:5432/atlas
      - REDIS_URL=redis://redis:6379/2

  # ... other services
```

### Service Startup

```bash
# Start all services
npm run services:start

# Start individual service
npm run service:start:nlds
npm run service:start:script
npm run service:start:atlas

# Health check all services
npm run services:health

# Stop all services
npm run services:stop
```

## 🧪 Testing

### Service Testing

```javascript
const ServiceTester = require('./shared/ServiceTester');

class NLDSTest extends ServiceTester {
  constructor() {
    super('NLDS', 'http://localhost:8000');
  }

  async testNLPProcessing() {
    const response = await this.post('/api/nlp/process', {
      command: 'test command'
    });
    
    this.assert(response.intent, 'Intent should be detected');
    this.assert(response.confidence > 0.5, 'Confidence should be > 0.5');
  }

  async testHealthEndpoint() {
    const health = await this.get('/health');
    this.assert(health.status === 'healthy', 'Service should be healthy');
  }
}
```

## 📚 Documentation

- **[N.L.D.S. Documentation](nlds/README.md)** - Natural Language Processing
- **[S.C.R.I.P.T. Documentation](script/README.md)** - Configuration Management
- **[A.T.L.A.S. Documentation](atlas/README.md)** - Resource Synchronization
- **[H.E.L.M. Documentation](helm/README.md)** - Performance Monitoring
- **[M.A.S.T.R. Documentation](mastr/README.md)** - Tool Forging
- **[A.S.C.E.N.D. Documentation](ascend/README.md)** - Agent Synthesis
- **[C.O.R.I. Documentation](cori/README.md)** - Cognitive Operations

## 🤝 Contributing

When contributing to services:

1. Follow the service architecture patterns
2. Implement comprehensive health checks
3. Add proper error handling and logging
4. Maintain API documentation
5. Include integration tests
6. Follow security best practices

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

---

**JAEGIS Services** - The distributed microservices foundation powering intelligent automation.