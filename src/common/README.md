# JAEGIS Common Utilities

**Shared utilities, frameworks, and components used across the JAEGIS-OS ecosystem**

The common module provides reusable components, utilities, and frameworks that are shared across all JAEGIS-OS services and applications. This ensures consistency, reduces code duplication, and provides a unified foundation for the entire ecosystem.

## 📁 Structure

```
src/common/
├── constants/                   # System-wide constants and configuration
│   ├── api.js                  # API endpoints and configuration
│   ├── errors.js               # Error codes and messages
│   ├── events.js               # Event types and names
│   ├── permissions.js          # Permission constants
│   └── services.js             # Service configuration
├── core/                       # Core shared functionality
│   ├── BaseService.js          # Base service class
│   ├── EventEmitter.js         # Enhanced event emitter
│   ├── Logger.js               # Centralized logging
│   ├── Validator.js            # Data validation utilities
│   └── Cache.js                # Caching utilities
├── frameworks/                 # Shared frameworks and protocols
│   ├── AgentFramework.js       # Agent development framework
│   ├── ServiceFramework.js     # Service development framework
│   ├── APIFramework.js         # API development framework
│   └── TestFramework.js        # Testing framework
├── models/                     # Data models and schemas
│   ├── Agent.js                # Agent data model
│   ├── Service.js              # Service data model
│   ├── User.js                 # User data model
│   ├── Task.js                 # Task data model
│   └── Event.js                # Event data model
├── utils/                      # Utility functions and helpers
│   ├── auth.js                 # Authentication utilities
│   ├── crypto.js               # Cryptographic utilities
│   ├── date.js                 # Date and time utilities
│   ├── file.js                 # File system utilities
│   ├── http.js                 # HTTP utilities
│   ├── network.js              # Network utilities
│   ├── parsing.js              # Data parsing utilities
│   ├── string.js               # String manipulation utilities
│   ├── validation.js           # Validation utilities
│   └── web-search.js           # Web search utilities
└── types/                      # TypeScript type definitions
    ├── agent.d.ts              # Agent type definitions
    ├── service.d.ts            # Service type definitions
    ├── api.d.ts                # API type definitions
    └── common.d.ts             # Common type definitions
```

## 🔧 Core Components

### BaseService Class

```javascript
const { BaseService } = require('@common/core/BaseService');

class MyService extends BaseService {
  constructor(config) {
    super('MyService', config);
  }

  async initialize() {
    await super.initialize();
    // Service-specific initialization
  }

  async healthCheck() {
    return {
      status: 'healthy',
      uptime: this.getUptime(),
      memory: process.memoryUsage()
    };
  }
}
```

### Logger

```javascript
const Logger = require('@common/core/Logger');

const logger = new Logger('ServiceName');

logger.info('Service started');
logger.error('Error occurred', { error: err });
logger.debug('Debug information', { data });
```

### Event System

```javascript
const { EventEmitter } = require('@common/core/EventEmitter');
const { EVENTS } = require('@common/constants/events');

class ServiceManager extends EventEmitter {
  async startService(serviceName) {
    this.emit(EVENTS.SERVICE_STARTING, { serviceName });
    // Start service logic
    this.emit(EVENTS.SERVICE_STARTED, { serviceName });
  }
}
```

## 🛡️ Security Utilities

### Authentication

```javascript
const { generateToken, verifyToken } = require('@common/utils/auth');
const { encrypt, decrypt } = require('@common/utils/crypto');

// JWT token management
const token = await generateToken(user, permissions);
const decoded = await verifyToken(token);

// Data encryption
const encrypted = encrypt(sensitiveData);
const decrypted = decrypt(encrypted);
```

### Validation

```javascript
const { Validator } = require('@common/core/Validator');
const { validateEmail, validatePassword } = require('@common/utils/validation');

const validator = new Validator({
  email: { required: true, validator: validateEmail },
  password: { required: true, validator: validatePassword }
});

const result = validator.validate(userData);
if (!result.isValid) {
  throw new Error(result.errors.join(', '));
}
```

## 📊 Data Models

### Agent Model

```javascript
const { Agent } = require('@common/models/Agent');

const agent = new Agent({
  id: 'agent-001',
  name: 'Research Agent',
  type: 'research',
  tier: 6,
  capabilities: ['web-search', 'data-analysis'],
  status: 'active'
});

await agent.save();
```

### Service Model

```javascript
const { Service } = require('@common/models/Service');

const service = new Service({
  name: 'N.L.D.S.',
  port: 8000,
  type: 'nlp',
  health: 'healthy',
  load: 45
});

await service.updateHealth();
```

## 🌐 Network Utilities

### HTTP Client

```javascript
const { HTTPClient } = require('@common/utils/http');

const client = new HTTPClient({
  baseURL: 'http://localhost:8000',
  timeout: 30000,
  retries: 3
});

const response = await client.get('/api/status');
const data = await client.post('/api/process', { command: 'test' });
```

### Service Discovery

```javascript
const { ServiceRegistry } = require('@common/utils/network');

const registry = new ServiceRegistry();

// Register service
await registry.register('nlds', {
  host: 'localhost',
  port: 8000,
  health: '/health'
});

// Discover service
const service = await registry.discover('nlds');
```

## 🔍 Parsing and Search

### Data Parsing

```javascript
const { parseJSON, parseXML, parseCSV } = require('@common/utils/parsing');

const data = parseJSON(jsonString);
const xml = parseXML(xmlString);
const csv = parseCSV(csvString);
```

### Web Search

```javascript
const { WebSearch } = require('@common/utils/web-search');

const search = new WebSearch();
const results = await search.query('JAEGIS AI system');
```

## 🧪 Testing Framework

### Test Utilities

```javascript
const { TestFramework } = require('@common/frameworks/TestFramework');

class ServiceTest extends TestFramework {
  async setup() {
    this.service = new MyService();
    await this.service.initialize();
  }

  async testHealthCheck() {
    const health = await this.service.healthCheck();
    this.assert(health.status === 'healthy');
  }

  async teardown() {
    await this.service.shutdown();
  }
}
```

## 📝 Constants and Configuration

### API Constants

```javascript
const { API_ENDPOINTS, HTTP_STATUS } = require('@common/constants/api');

// Use predefined endpoints
const response = await fetch(API_ENDPOINTS.NLDS.PROCESS);

// Use status codes
if (response.status === HTTP_STATUS.OK) {
  // Handle success
}
```

### Error Handling

```javascript
const { ERROR_CODES, createError } = require('@common/constants/errors');

throw createError(ERROR_CODES.VALIDATION_FAILED, 'Invalid input data');
```

## 🔄 Caching

### Cache Utilities

```javascript
const { Cache } = require('@common/core/Cache');

const cache = new Cache({
  ttl: 300, // 5 minutes
  maxSize: 1000
});

await cache.set('key', data);
const cached = await cache.get('key');
```

## 📅 Date and Time

### Date Utilities

```javascript
const { formatDate, parseDate, getTimestamp } = require('@common/utils/date');

const formatted = formatDate(new Date(), 'YYYY-MM-DD HH:mm:ss');
const parsed = parseDate('2025-08-02T16:00:00Z');
const timestamp = getTimestamp();
```

## 🔧 File System

### File Utilities

```javascript
const { readFile, writeFile, ensureDir } = require('@common/utils/file');

await ensureDir('/path/to/directory');
const content = await readFile('/path/to/file.txt');
await writeFile('/path/to/output.txt', content);
```

## 🎯 Usage Examples

### Service Integration

```javascript
const { BaseService } = require('@common/core/BaseService');
const { Logger } = require('@common/core/Logger');
const { HTTPClient } = require('@common/utils/http');

class NLDSService extends BaseService {
  constructor() {
    super('NLDS', { port: 8000 });
    this.logger = new Logger('NLDS');
    this.client = new HTTPClient();
  }

  async processCommand(command) {
    this.logger.info('Processing command', { command });
    
    try {
      const result = await this.nlp.process(command);
      this.emit('command_processed', { command, result });
      return result;
    } catch (error) {
      this.logger.error('Command processing failed', { error });
      throw error;
    }
  }
}
```

### Agent Development

```javascript
const { AgentFramework } = require('@common/frameworks/AgentFramework');
const { Agent } = require('@common/models/Agent');

class ResearchAgent extends AgentFramework {
  constructor() {
    super({
      name: 'Research Agent',
      type: 'research',
      capabilities: ['web-search', 'data-analysis']
    });
  }

  async executeTask(task) {
    const agent = new Agent(this.config);
    return await agent.process(task);
  }
}
```

## 🚀 Getting Started

### Installation

```bash
# Install common utilities
npm install @jaegis/common

# Or use in development
npm link ../common
```

### Usage

```javascript
// Import specific utilities
const { Logger } = require('@jaegis/common/core/Logger');
const { validateEmail } = require('@jaegis/common/utils/validation');

// Import entire modules
const constants = require('@jaegis/common/constants');
const utils = require('@jaegis/common/utils');
```

## 🧪 Testing

```bash
# Run common utilities tests
npm run test:common

# Run specific test suites
npm run test:common:core
npm run test:common:utils
npm run test:common:models
```

## 📚 Documentation

- **[API Reference](docs/api.md)** - Complete API documentation
- **[Examples](examples/)** - Usage examples and patterns
- **[Migration Guide](docs/migration.md)** - Upgrading between versions

## 🤝 Contributing

When contributing to common utilities:

1. Ensure backward compatibility
2. Add comprehensive tests
3. Update documentation
4. Follow coding standards
5. Consider impact on all services

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

---

**JAEGIS Common** - Shared foundation for the JAEGIS-OS ecosystem.