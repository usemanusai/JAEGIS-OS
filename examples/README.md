# JAEGIS-OS Examples

**Practical examples and code samples for the JAEGIS-OS ecosystem**

This directory contains comprehensive examples, tutorials, and code samples to help you understand and implement various features of the JAEGIS-OS ecosystem. From basic usage to advanced integrations, these examples provide practical guidance for developers, researchers, and system administrators.

## 📁 Examples Structure

```
examples/
├── README.md                    # This file - Examples overview
├── basic-usage/                 # Basic usage examples
│   ├── getting-started/        # Getting started examples
│   ├── authentication/         # Authentication examples
│   ├── service-calls/          # Basic service API calls
│   └── web-os-basics/          # Web OS desktop basics
├── advanced-features/           # Advanced feature examples
│   ├── agent-coordination/     # Multi-agent coordination
│   ├── real-time-updates/      # Real-time communication
│   ├── performance-optimization/ # Performance tuning
│   └── custom-integrations/    # Custom integration patterns
├── integrations/                # External integration examples
│   ├── github-integration/     # GitHub integration examples
│   ├── mcp-integration/        # MCP integration examples
│   ├── openrouter-integration/ # OpenRouter AI integration
│   └── vscode-integration/     # VSCode integration examples
├── custom-development/          # Custom development examples
│   ├── building-agents/        # Custom agent development
│   ├── creating-services/      # New service development
│   ├── web-os-applications/    # Web OS app development
│   └── testing-examples/       # Testing and validation
├── deployment/                  # Deployment examples
│   ├── docker-compose/         # Docker deployment examples
│   ├── kubernetes/             # Kubernetes deployment
│   ├── cloud-deployment/       # Cloud platform deployment
│   └── monitoring-setup/       # Monitoring configuration
├── use-cases/                   # Real-world use case examples
│   ├── research-automation/    # Research workflow automation
│   ├── development-workflow/   # Software development automation
│   ├── data-analysis/          # Data analysis pipelines
│   └── business-automation/    # Business process automation
└── tutorials/                   # Step-by-step tutorials
    ├── 01-first-steps/         # First steps with JAEGIS-OS
    ├── 02-building-agents/     # Building your first agent
    ├── 03-service-integration/ # Integrating services
    └── 04-advanced-features/   # Advanced feature usage
```

## 🚀 Quick Start Examples

### Basic Service API Call
```javascript
// examples/basic-usage/service-calls/nlds-basic.js
const axios = require('axios');

async function processNaturalLanguageCommand() {
  try {
    const response = await axios.post('http://localhost:8000/api/nlp/process', {
      command: 'open file explorer',
      context: 'desktop_environment'
    });
    
    console.log('Intent:', response.data.intent);
    console.log('Confidence:', response.data.confidence);
    console.log('Action:', response.data.action);
    
    return response.data;
  } catch (error) {
    console.error('Error processing command:', error.message);
    throw error;
  }
}

// Usage
processNaturalLanguageCommand()
  .then(result => console.log('Command processed successfully:', result))
  .catch(error => console.error('Failed to process command:', error));
```

### Authentication Example
```javascript
// examples/basic-usage/authentication/login-example.js
const axios = require('axios');

class JAEGISAuth {
  constructor(baseURL = 'http://localhost:3000') {
    this.baseURL = baseURL;
    this.token = null;
    this.refreshToken = null;
  }
  
  async login(username, password) {
    try {
      const response = await axios.post(`${this.baseURL}/api/auth/login`, {
        username,
        password
      });
      
      this.token = response.data.token;
      this.refreshToken = response.data.refreshToken;
      
      console.log('Login successful');
      console.log('User:', response.data.user);
      console.log('Permissions:', response.data.user.permissions);
      
      return response.data;
    } catch (error) {
      console.error('Login failed:', error.response?.data?.error || error.message);
      throw error;
    }
  }
  
  async callProtectedAPI(endpoint, data = {}) {
    if (!this.token) {
      throw new Error('Not authenticated. Please login first.');
    }
    
    try {
      const response = await axios.post(`${this.baseURL}${endpoint}`, data, {
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      return response.data;
    } catch (error) {
      if (error.response?.status === 401) {
        console.log('Token expired, attempting refresh...');
        await this.refreshAccessToken();
        return this.callProtectedAPI(endpoint, data);
      }
      throw error;
    }
  }
  
  async refreshAccessToken() {
    try {
      const response = await axios.post(`${this.baseURL}/api/auth/refresh`, {
        refreshToken: this.refreshToken
      });
      
      this.token = response.data.token;
      console.log('Token refreshed successfully');
      
      return response.data;
    } catch (error) {
      console.error('Token refresh failed:', error.message);
      this.token = null;
      this.refreshToken = null;
      throw error;
    }
  }
}

// Usage example
async function authenticationExample() {
  const auth = new JAEGISAuth();
  
  // Login
  await auth.login('admin', 'admin');
  
  // Call protected API
  const metrics = await auth.callProtectedAPI('/api/protected/metrics');
  console.log('Protected data:', metrics);
}

authenticationExample().catch(console.error);
```

## 🤖 Agent Development Examples

### Building a Custom Research Agent
```python
# examples/custom-development/building-agents/research-agent.py
import asyncio
import aiohttp
from typing import Dict, List, Any

class ResearchAgent:
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.capabilities = ['web-search', 'data-analysis', 'report-generation']
        self.status = 'idle'
        
    async def initialize(self):
        """Initialize the research agent"""
        print(f"Initializing Research Agent: {self.name}")
        self.status = 'ready'
        
        # Register with A.S.C.E.N.D. service
        await self.register_with_ascend()
        
    async def register_with_ascend(self):
        """Register agent with A.S.C.E.N.D. service"""
        registration_data = {
            'agent_id': self.agent_id,
            'name': self.name,
            'type': 'research',
            'tier': 6,
            'capabilities': self.capabilities,
            'status': self.status
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'http://localhost:8084/api/agents/register',
                json=registration_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"Agent registered successfully: {result}")
                else:
                    print(f"Registration failed: {response.status}")
    
    async def execute_research_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a research task"""
        self.status = 'working'
        
        try:
            query = task.get('query', '')
            research_type = task.get('type', 'general')
            
            print(f"Starting research on: {query}")
            
            # Step 1: Web search
            search_results = await self.perform_web_search(query)
            
            # Step 2: Analyze results
            analysis = await self.analyze_search_results(search_results)
            
            # Step 3: Generate report
            report = await self.generate_report(query, analysis)
            
            result = {
                'agent_id': self.agent_id,
                'task_id': task.get('task_id'),
                'status': 'completed',
                'query': query,
                'search_results_count': len(search_results),
                'analysis': analysis,
                'report': report,
                'timestamp': asyncio.get_event_loop().time()
            }
            
            self.status = 'ready'
            return result
            
        except Exception as error:
            self.status = 'error'
            return {
                'agent_id': self.agent_id,
                'task_id': task.get('task_id'),
                'status': 'error',
                'error': str(error),
                'timestamp': asyncio.get_event_loop().time()
            }
    
    async def perform_web_search(self, query: str) -> List[Dict[str, Any]]:
        """Perform web search using integrated search service"""
        # This would integrate with the web search service
        # For demo purposes, returning mock data
        return [
            {
                'title': f'Research result for {query}',
                'url': 'https://example.com/research',
                'snippet': f'Detailed information about {query}...',
                'relevance_score': 0.95
            }
        ]
    
    async def analyze_search_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze search results using C.O.R.I. cognitive operations"""
        analysis_request = {
            'task': 'analyze_research_data',
            'data': results,
            'analysis_type': 'comprehensive'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'http://localhost:8085/api/cognitive/process',
                json=analysis_request
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {'error': 'Analysis failed', 'status': response.status}
    
    async def generate_report(self, query: str, analysis: Dict[str, Any]) -> str:
        """Generate research report"""
        report = f"""
# Research Report: {query}

## Executive Summary
Based on comprehensive research and analysis, the following findings were identified:

## Key Findings
{analysis.get('summary', 'Analysis summary not available')}

## Detailed Analysis
{analysis.get('detailed_analysis', 'Detailed analysis not available')}

## Recommendations
{analysis.get('recommendations', 'No specific recommendations available')}

## Sources
- {len(analysis.get('sources', []))} sources analyzed
- Confidence score: {analysis.get('confidence', 'N/A')}

Generated by JAEGIS Research Agent: {self.name}
Agent ID: {self.agent_id}
"""
        return report

# Usage example
async def research_agent_example():
    # Create and initialize research agent
    agent = ResearchAgent('research-001', 'AI Research Agent')
    await agent.initialize()
    
    # Execute research task
    task = {
        'task_id': 'task-001',
        'query': 'Latest developments in AI and machine learning',
        'type': 'technology_research'
    }
    
    result = await agent.execute_research_task(task)
    print("Research completed:")
    print(f"Status: {result['status']}")
    if result['status'] == 'completed':
        print(f"Report:\n{result['report']}")
    else:
        print(f"Error: {result.get('error')}")

# Run the example
if __name__ == "__main__":
    asyncio.run(research_agent_example())
```

## 🔗 Integration Examples

### GitHub Integration Example
```javascript
// examples/integrations/github-integration/repository-automation.js
const { Octokit } = require('@octokit/rest');

class GitHubAutomation {
  constructor(token) {
    this.octokit = new Octokit({
      auth: token
    });
  }
  
  async createProjectRepository(projectData) {
    try {
      // Create repository
      const repo = await this.octokit.repos.create({
        name: projectData.name,
        description: projectData.description,
        private: projectData.private || false,
        auto_init: true
      });
      
      console.log(`Repository created: ${repo.data.html_url}`);
      
      // Set up project structure
      await this.setupProjectStructure(projectData.name, projectData.structure);
      
      // Create initial issues
      if (projectData.issues) {
        await this.createInitialIssues(projectData.name, projectData.issues);
      }
      
      // Set up GitHub Actions
      if (projectData.cicd) {
        await this.setupGitHubActions(projectData.name, projectData.cicd);
      }
      
      return repo.data;
    } catch (error) {
      console.error('Failed to create repository:', error.message);
      throw error;
    }
  }
  
  async setupProjectStructure(repoName, structure) {
    const owner = 'usemanusai'; // Replace with actual owner
    
    for (const file of structure.files) {
      await this.octokit.repos.createOrUpdateFileContents({
        owner,
        repo: repoName,
        path: file.path,
        message: `Add ${file.path}`,
        content: Buffer.from(file.content).toString('base64')
      });
    }
    
    console.log('Project structure created');
  }
  
  async createInitialIssues(repoName, issues) {
    const owner = 'usemanusai';
    
    for (const issue of issues) {
      await this.octokit.issues.create({
        owner,
        repo: repoName,
        title: issue.title,
        body: issue.body,
        labels: issue.labels || []
      });
    }
    
    console.log(`Created ${issues.length} initial issues`);
  }
  
  async setupGitHubActions(repoName, cicdConfig) {
    const owner = 'usemanusai';
    
    const workflowContent = `
name: ${cicdConfig.name}

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm install
        
      - name: Run tests
        run: npm test
        
      - name: Build project
        run: npm run build
`;
    
    await this.octokit.repos.createOrUpdateFileContents({
      owner,
      repo: repoName,
      path: '.github/workflows/ci.yml',
      message: 'Add CI/CD workflow',
      content: Buffer.from(workflowContent).toString('base64')
    });
    
    console.log('GitHub Actions workflow created');
  }
}

// Usage example
async function githubIntegrationExample() {
  const github = new GitHubAutomation(process.env.GITHUB_TOKEN);
  
  const projectData = {
    name: 'jaegis-example-project',
    description: 'Example project created with JAEGIS automation',
    private: false,
    structure: {
      files: [
        {
          path: 'README.md',
          content: '# JAEGIS Example Project\n\nThis project was created using JAEGIS automation.'
        },
        {
          path: 'package.json',
          content: JSON.stringify({
            name: 'jaegis-example-project',
            version: '1.0.0',
            description: 'Example project',
            main: 'index.js',
            scripts: {
              test: 'jest',
              build: 'webpack'
            }
          }, null, 2)
        }
      ]
    },
    issues: [
      {
        title: 'Setup project documentation',
        body: 'Create comprehensive documentation for the project',
        labels: ['documentation', 'enhancement']
      },
      {
        title: 'Implement core functionality',
        body: 'Implement the main features of the project',
        labels: ['feature', 'high-priority']
      }
    ],
    cicd: {
      name: 'CI/CD Pipeline'
    }
  };
  
  const repository = await github.createProjectRepository(projectData);
  console.log('Project automation completed:', repository.html_url);
}

githubIntegrationExample().catch(console.error);
```

### OpenRouter AI Integration Example
```javascript
// examples/integrations/openrouter-integration/ai-assistant.js
const axios = require('axios');

class OpenRouterAIAssistant {
  constructor(apiKey, appName = 'JAEGIS-OS') {
    this.apiKey = apiKey;
    this.appName = appName;
    this.baseURL = 'https://openrouter.ai/api/v1';
  }
  
  async generateCompletion(prompt, options = {}) {
    const defaultOptions = {
      model: 'anthropic/claude-3.5-sonnet',
      max_tokens: 1000,
      temperature: 0.7,
      stream: false
    };
    
    const requestOptions = { ...defaultOptions, ...options };
    
    try {
      const response = await axios.post(`${this.baseURL}/chat/completions`, {
        model: requestOptions.model,
        messages: [
          { role: 'user', content: prompt }
        ],
        max_tokens: requestOptions.max_tokens,
        temperature: requestOptions.temperature,
        stream: requestOptions.stream
      }, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'HTTP-Referer': 'https://github.com/usemanusai/JAEGIS-OS',
          'X-Title': this.appName,
          'Content-Type': 'application/json'
        }
      });
      
      return response.data.choices[0].message.content;
    } catch (error) {
      console.error('AI completion failed:', error.response?.data || error.message);
      throw error;
    }
  }
  
  async generateCode(description, language = 'javascript') {
    const prompt = `Generate ${language} code for the following requirement:

${description}

Please provide clean, well-commented code that follows best practices.`;
    
    return await this.generateCompletion(prompt, {
      model: 'anthropic/claude-3.5-sonnet',
      max_tokens: 2000,
      temperature: 0.3
    });
  }
  
  async analyzeCode(code, language = 'javascript') {
    const prompt = `Analyze the following ${language} code and provide feedback on:
1. Code quality and best practices
2. Potential bugs or issues
3. Performance optimizations
4. Security considerations

Code:
\`\`\`${language}
${code}
\`\`\``;
    
    return await this.generateCompletion(prompt, {
      model: 'anthropic/claude-3.5-sonnet',
      max_tokens: 1500,
      temperature: 0.2
    });
  }
  
  async generateDocumentation(code, language = 'javascript') {
    const prompt = `Generate comprehensive documentation for the following ${language} code:

\`\`\`${language}
${code}
\`\`\`

Include:
- Function/class descriptions
- Parameter documentation
- Return value descriptions
- Usage examples
- Any important notes or warnings`;
    
    return await this.generateCompletion(prompt, {
      model: 'anthropic/claude-3.5-sonnet',
      max_tokens: 2000,
      temperature: 0.4
    });
  }
  
  async streamCompletion(prompt, onChunk, onComplete) {
    try {
      const response = await axios.post(`${this.baseURL}/chat/completions`, {
        model: 'anthropic/claude-3.5-sonnet',
        messages: [
          { role: 'user', content: prompt }
        ],
        max_tokens: 1000,
        temperature: 0.7,
        stream: true
      }, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'HTTP-Referer': 'https://github.com/usemanusai/JAEGIS-OS',
          'X-Title': this.appName,
          'Content-Type': 'application/json'
        },
        responseType: 'stream'
      });
      
      response.data.on('data', (chunk) => {
        const lines = chunk.toString().split('\n');
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') {
              onComplete();
              return;
            }
            
            try {
              const parsed = JSON.parse(data);
              const content = parsed.choices[0]?.delta?.content;
              if (content) {
                onChunk(content);
              }
            } catch (error) {
              // Ignore parsing errors for incomplete chunks
            }
          }
        }
      });
      
    } catch (error) {
      console.error('Streaming completion failed:', error.message);
      throw error;
    }
  }
}

// Usage examples
async function aiAssistantExamples() {
  const assistant = new OpenRouterAIAssistant(process.env.OPENROUTER_API_KEY);
  
  // Example 1: Generate code
  console.log('Generating code...');
  const code = await assistant.generateCode(
    'Create a React component for a todo list with add, delete, and toggle functionality',
    'javascript'
  );
  console.log('Generated code:', code);
  
  // Example 2: Analyze code
  console.log('\nAnalyzing code...');
  const analysis = await assistant.analyzeCode(`
function calculateTotal(items) {
  var total = 0;
  for (var i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
  }
  return total;
}
  `, 'javascript');
  console.log('Code analysis:', analysis);
  
  // Example 3: Generate documentation
  console.log('\nGenerating documentation...');
  const docs = await assistant.generateDocumentation(`
class UserManager {
  constructor(database) {
    this.db = database;
  }
  
  async createUser(userData) {
    const user = await this.db.users.create(userData);
    return user;
  }
  
  async getUserById(id) {
    return await this.db.users.findById(id);
  }
}
  `, 'javascript');
  console.log('Generated documentation:', docs);
  
  // Example 4: Streaming completion
  console.log('\nStreaming completion...');
  let streamedContent = '';
  await assistant.streamCompletion(
    'Explain the benefits of using JAEGIS-OS for AI development',
    (chunk) => {
      process.stdout.write(chunk);
      streamedContent += chunk;
    },
    () => {
      console.log('\n\nStreaming completed');
      console.log('Full content length:', streamedContent.length);
    }
  );
}

aiAssistantExamples().catch(console.error);
```

## 🖥️ Web OS Application Development

### Creating a Custom Desktop Application
```javascript
// examples/custom-development/web-os-applications/custom-app.jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useWebSocket } from '../hooks/useWebSocket';

const CustomCalculatorApp = ({ windowId, onClose, onMinimize, onMaximize }) => {
  const [display, setDisplay] = useState('0');
  const [previousValue, setPreviousValue] = useState(null);
  const [operation, setOperation] = useState(null);
  const [waitingForOperand, setWaitingForOperand] = useState(false);
  
  const { user } = useAuth();
  const { socket } = useWebSocket();
  
  useEffect(() => {
    // Register app with system
    socket.emit('app_opened', {
      appName: 'Custom Calculator',
      windowId,
      userId: user?.id
    });
    
    return () => {
      socket.emit('app_closed', {
        appName: 'Custom Calculator',
        windowId,
        userId: user?.id
      });
    };
  }, [socket, windowId, user]);
  
  const inputNumber = (num) => {
    if (waitingForOperand) {
      setDisplay(String(num));
      setWaitingForOperand(false);
    } else {
      setDisplay(display === '0' ? String(num) : display + num);
    }
  };
  
  const inputOperation = (nextOperation) => {
    const inputValue = parseFloat(display);
    
    if (previousValue === null) {
      setPreviousValue(inputValue);
    } else if (operation) {
      const currentValue = previousValue || 0;
      const newValue = calculate(currentValue, inputValue, operation);
      
      setDisplay(String(newValue));
      setPreviousValue(newValue);
    }
    
    setWaitingForOperand(true);
    setOperation(nextOperation);
  };
  
  const calculate = (firstValue, secondValue, operation) => {
    switch (operation) {
      case '+':
        return firstValue + secondValue;
      case '-':
        return firstValue - secondValue;
      case '*':
        return firstValue * secondValue;
      case '/':
        return firstValue / secondValue;
      case '=':
        return secondValue;
      default:
        return secondValue;
    }
  };
  
  const performCalculation = () => {
    const inputValue = parseFloat(display);
    
    if (previousValue !== null && operation) {
      const newValue = calculate(previousValue, inputValue, operation);
      setDisplay(String(newValue));
      setPreviousValue(null);
      setOperation(null);
      setWaitingForOperand(true);
      
      // Log calculation to system
      socket.emit('calculation_performed', {
        operation: `${previousValue} ${operation} ${inputValue} = ${newValue}`,
        userId: user?.id,
        timestamp: new Date().toISOString()
      });
    }
  };
  
  const clear = () => {
    setDisplay('0');
    setPreviousValue(null);
    setOperation(null);
    setWaitingForOperand(false);
  };
  
  return (
    <div className="calculator-app bg-white rounded-lg shadow-lg p-4 w-80">
      {/* Window controls */}
      <div className="window-controls flex justify-between items-center mb-4 pb-2 border-b">
        <h3 className="text-lg font-semibold">Custom Calculator</h3>
        <div className="flex space-x-2">
          <button
            onClick={onMinimize}
            className="w-3 h-3 bg-yellow-500 rounded-full hover:bg-yellow-600"
          />
          <button
            onClick={onMaximize}
            className="w-3 h-3 bg-green-500 rounded-full hover:bg-green-600"
          />
          <button
            onClick={onClose}
            className="w-3 h-3 bg-red-500 rounded-full hover:bg-red-600"
          />
        </div>
      </div>
      
      {/* Display */}
      <div className="display bg-gray-900 text-white text-right text-2xl p-4 rounded mb-4 font-mono">
        {display}
      </div>
      
      {/* Buttons */}
      <div className="buttons grid grid-cols-4 gap-2">
        <button
          onClick={clear}
          className="col-span-2 bg-gray-500 hover:bg-gray-600 text-white p-3 rounded"
        >
          Clear
        </button>
        <button
          onClick={() => inputOperation('/')}
          className="bg-orange-500 hover:bg-orange-600 text-white p-3 rounded"
        >
          ÷
        </button>
        <button
          onClick={() => inputOperation('*')}
          className="bg-orange-500 hover:bg-orange-600 text-white p-3 rounded"
        >
          ×
        </button>
        
        {[7, 8, 9].map(num => (
          <button
            key={num}
            onClick={() => inputNumber(num)}
            className="bg-gray-300 hover:bg-gray-400 text-black p-3 rounded"
          >
            {num}
          </button>
        ))}
        <button
          onClick={() => inputOperation('-')}
          className="bg-orange-500 hover:bg-orange-600 text-white p-3 rounded"
        >
          −
        </button>
        
        {[4, 5, 6].map(num => (
          <button
            key={num}
            onClick={() => inputNumber(num)}
            className="bg-gray-300 hover:bg-gray-400 text-black p-3 rounded"
          >
            {num}
          </button>
        ))}
        <button
          onClick={() => inputOperation('+')}
          className="bg-orange-500 hover:bg-orange-600 text-white p-3 rounded"
        >
          +
        </button>
        
        {[1, 2, 3].map(num => (
          <button
            key={num}
            onClick={() => inputNumber(num)}
            className="bg-gray-300 hover:bg-gray-400 text-black p-3 rounded"
          >
            {num}
          </button>
        ))}
        <button
          onClick={performCalculation}
          className="row-span-2 bg-orange-500 hover:bg-orange-600 text-white p-3 rounded"
        >
          =
        </button>
        
        <button
          onClick={() => inputNumber(0)}
          className="col-span-2 bg-gray-300 hover:bg-gray-400 text-black p-3 rounded"
        >
          0
        </button>
        <button
          onClick={() => setDisplay(display + '.')}
          className="bg-gray-300 hover:bg-gray-400 text-black p-3 rounded"
        >
          .
        </button>
      </div>
    </div>
  );
};

// App registration for the Web OS
export const CustomCalculatorAppConfig = {
  id: 'custom-calculator',
  name: 'Custom Calculator',
  icon: '🧮',
  category: 'Utilities',
  component: CustomCalculatorApp,
  defaultSize: { width: 320, height: 480 },
  resizable: false,
  permissions: ['basic_access']
};

export default CustomCalculatorApp;
```

## 🔄 Real-time Communication Example
```javascript
// examples/advanced-features/real-time-updates/websocket-client.js
class JAEGISWebSocketClient {
  constructor(url = 'ws://localhost:8000') {
    this.url = url;
    this.socket = null;
    this.eventHandlers = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }
  
  connect() {
    return new Promise((resolve, reject) => {
      try {
        this.socket = new WebSocket(this.url);
        
        this.socket.onopen = (event) => {
          console.log('WebSocket connected');
          this.reconnectAttempts = 0;
          this.emit('connected', event);
          resolve(event);
        };
        
        this.socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error);
          }
        };
        
        this.socket.onclose = (event) => {
          console.log('WebSocket disconnected');
          this.emit('disconnected', event);
          this.attemptReconnect();
        };
        
        this.socket.onerror = (error) => {
          console.error('WebSocket error:', error);
          this.emit('error', error);
          reject(error);
        };
        
      } catch (error) {
        reject(error);
      }
    });
  }
  
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
  
  send(type, data) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      const message = {
        type,
        data,
        timestamp: new Date().toISOString()
      };
      this.socket.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket not connected. Message not sent:', { type, data });
    }
  }
  
  on(event, handler) {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, []);
    }
    this.eventHandlers.get(event).push(handler);
  }
  
  off(event, handler) {
    if (this.eventHandlers.has(event)) {
      const handlers = this.eventHandlers.get(event);
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
  }
  
  emit(event, data) {
    if (this.eventHandlers.has(event)) {
      this.eventHandlers.get(event).forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error(`Error in event handler for ${event}:`, error);
        }
      });
    }
  }
  
  handleMessage(message) {
    const { type, data } = message;
    
    switch (type) {
      case 'service_status_update':
        this.emit('service_status', data);
        break;
      case 'agent_task_completed':
        this.emit('agent_task', data);
        break;
      case 'system_notification':
        this.emit('notification', data);
        break;
      case 'real_time_metrics':
        this.emit('metrics', data);
        break;
      default:
        this.emit(type, data);
    }
  }
  
  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
      
      console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect().catch(error => {
          console.error('Reconnection failed:', error);
        });
      }, delay);
    } else {
      console.error('Max reconnection attempts reached. Please refresh the page.');
      this.emit('max_reconnect_attempts_reached');
    }
  }
  
  // Convenience methods for common operations
  subscribeToServiceUpdates() {
    this.send('subscribe', { type: 'service_updates' });
  }
  
  subscribeToAgentTasks() {
    this.send('subscribe', { type: 'agent_tasks' });
  }
  
  subscribeToSystemMetrics() {
    this.send('subscribe', { type: 'system_metrics' });
  }
  
  requestServiceStatus() {
    this.send('request', { type: 'service_status' });
  }
  
  requestSystemMetrics() {
    this.send('request', { type: 'system_metrics' });
  }
}

// Usage example
async function realTimeExample() {
  const wsClient = new JAEGISWebSocketClient();
  
  // Set up event handlers
  wsClient.on('connected', () => {
    console.log('Connected to JAEGIS WebSocket server');
    
    // Subscribe to updates
    wsClient.subscribeToServiceUpdates();
    wsClient.subscribeToAgentTasks();
    wsClient.subscribeToSystemMetrics();
  });
  
  wsClient.on('service_status', (status) => {
    console.log('Service status update:', status);
    updateServiceStatusUI(status);
  });
  
  wsClient.on('agent_task', (task) => {
    console.log('Agent task completed:', task);
    updateAgentTaskUI(task);
  });
  
  wsClient.on('metrics', (metrics) => {
    console.log('System metrics update:', metrics);
    updateMetricsUI(metrics);
  });
  
  wsClient.on('notification', (notification) => {
    console.log('System notification:', notification);
    showNotification(notification);
  });
  
  wsClient.on('disconnected', () => {
    console.log('Disconnected from WebSocket server');
    showConnectionStatus('disconnected');
  });
  
  wsClient.on('max_reconnect_attempts_reached', () => {
    showErrorMessage('Connection lost. Please refresh the page.');
  });
  
  // Connect to server
  try {
    await wsClient.connect();
  } catch (error) {
    console.error('Failed to connect to WebSocket server:', error);
  }
  
  // Example UI update functions (implement based on your UI framework)
  function updateServiceStatusUI(status) {
    // Update service status indicators in the UI
    const serviceElement = document.getElementById(`service-${status.service}`);
    if (serviceElement) {
      serviceElement.className = `service-indicator ${status.health}`;
      serviceElement.textContent = `${status.service}: ${status.health} (${status.load}%)`;
    }
  }
  
  function updateAgentTaskUI(task) {
    // Update agent task list in the UI
    const taskList = document.getElementById('agent-tasks');
    if (taskList) {
      const taskElement = document.createElement('div');
      taskElement.className = 'task-item';
      taskElement.innerHTML = `
        <span class="task-agent">${task.agent_id}</span>
        <span class="task-status ${task.status}">${task.status}</span>
        <span class="task-time">${new Date(task.timestamp).toLocaleTimeString()}</span>
      `;
      taskList.prepend(taskElement);
      
      // Keep only last 10 tasks
      while (taskList.children.length > 10) {
        taskList.removeChild(taskList.lastChild);
      }
    }
  }
  
  function updateMetricsUI(metrics) {
    // Update system metrics charts/displays
    document.getElementById('cpu-usage').textContent = `${metrics.cpu.usage}%`;
    document.getElementById('memory-usage').textContent = `${metrics.memory.used}MB`;
    document.getElementById('network-io').textContent = `${metrics.network.bytesPerSecond} B/s`;
  }
  
  function showNotification(notification) {
    // Show system notification
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(notification.title, {
        body: notification.message,
        icon: '/icons/jaegis-icon.png'
      });
    }
  }
  
  function showConnectionStatus(status) {
    const statusElement = document.getElementById('connection-status');
    if (statusElement) {
      statusElement.className = `connection-status ${status}`;
      statusElement.textContent = status === 'connected' ? 'Connected' : 'Disconnected';
    }
  }
  
  function showErrorMessage(message) {
    const errorElement = document.getElementById('error-message');
    if (errorElement) {
      errorElement.textContent = message;
      errorElement.style.display = 'block';
    }
  }
  
  return wsClient;
}

// Initialize real-time connection
realTimeExample().catch(console.error);
```

## 📚 More Examples

### Available Example Categories

1. **[Basic Usage Examples](basic-usage/)** - Getting started with JAEGIS-OS
2. **[Advanced Features](advanced-features/)** - Complex functionality and patterns
3. **[Integration Examples](integrations/)** - External system integrations
4. **[Custom Development](custom-development/)** - Building custom components
5. **[Deployment Examples](deployment/)** - Production deployment scenarios
6. **[Use Case Examples](use-cases/)** - Real-world application scenarios
7. **[Tutorial Series](tutorials/)** - Step-by-step learning guides

### Running the Examples

```bash
# Clone the repository
git clone https://github.com/usemanusai/JAEGIS-OS.git
cd JAEGIS-OS

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run basic examples
npm run examples:basic

# Run integration examples
npm run examples:integrations

# Run custom development examples
npm run examples:custom

# Run all examples
npm run examples:all
```

### Environment Setup for Examples

```bash
# Required environment variables for examples
export GITHUB_TOKEN="your_github_token"
export OPENROUTER_API_KEY="your_openrouter_api_key"
export JAEGIS_API_BASE_URL="http://localhost:8000"
export JAEGIS_WS_URL="ws://localhost:8000"

# Optional environment variables
export JAEGIS_DEBUG="true"
export JAEGIS_LOG_LEVEL="debug"
```

## 🤝 Contributing Examples

We welcome contributions of new examples! Please:

1. Follow the existing example structure and naming conventions
2. Include comprehensive comments and documentation
3. Provide a README.md for each example directory
4. Test your examples thoroughly
5. Submit a pull request with a clear description

## 📄 License

These examples are licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**JAEGIS-OS Examples** - Learn by doing with practical, real-world examples.