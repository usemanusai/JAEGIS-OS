#!/usr/bin/env node

/**
 * JAEGIS-OS - Complete Standalone Deployment
 * AI-Powered Operating System for Free HTTPS Hosting
 * 
 * This single file contains everything needed to deploy JAEGIS-OS
 * Just copy this file and run: node jaegis-os-complete.js
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

// JAEGIS-OS Core Implementation
class JAEGISCore {
  constructor() {
    this.systemStatus = {
      running: true,
      uptime: Date.now(),
      memory: { used: 0, total: 100 },
      cpu: { usage: 0 },
      processes: []
    };
    this.fileSystem = new FileSystem();
    this.terminal = new Terminal();
    this.ai = new AIInterface();
  }

  async executeCommand(command, args = []) {
    console.log(`Executing command: ${command}`, args);
    
    switch (command.toLowerCase()) {
      case 'help':
        return this.showHelp();
      case 'status':
        return this.getStatus();
      case 'ls':
        return this.fileSystem.listFiles(args[0] || '/');
      case 'mkdir':
        return this.fileSystem.createDirectory(args[0]);
      case 'write':
        return this.fileSystem.writeFile(args[0], args.slice(1).join(' '));
      case 'read':
        return this.fileSystem.readFile(args[0]);
      case 'ai':
        return this.ai.processQuery(args.join(' '));
      case 'clear':
        return this.terminal.clear();
      default:
        return `Unknown command: ${command}. Type 'help' for available commands.`;
    }
  }

  showHelp() {
    return `
JAEGIS-OS Commands:
  help              - Show this help message
  status            - Show system status
  ls [path]         - List files in directory
  mkdir <name>      - Create a directory
  write <file> <content> - Write content to file
  read <file>       - Read file contents
  ai <query>        - Ask AI assistant
  clear             - Clear terminal
    `.trim();
  }

  getStatus() {
    const uptime = Math.floor((Date.now() - this.systemStatus.uptime) / 1000);
    return `System Status:
  Running: ${this.systemStatus.running}
  Uptime: ${uptime}s
  Memory: ${this.systemStatus.memory.used}MB / ${this.systemStatus.memory.total}MB
  CPU: ${this.systemStatus.cpu.usage}%
  Processes: ${this.systemStatus.processes.length}`;
  }
}

// File System Implementation
class FileSystem {
  constructor() {
    this.basePath = '/tmp/jaos-fs';
    this.ensureBasePath();
  }

  ensureBasePath() {
    try {
      if (!fs.existsSync(this.basePath)) {
        fs.mkdirSync(this.basePath, { recursive: true });
      }
    } catch (error) {
      console.log('Using in-memory file system');
      this.files = {};
      this.directories = { '/': [] };
    }
  }

  listFiles(dirPath = '/') {
    try {
      const fullPath = path.join(this.basePath, dirPath);
      if (fs.existsSync(fullPath)) {
        const items = fs.readdirSync(fullPath);
        return items.map(item => {
          const itemPath = path.join(fullPath, item);
          const stats = fs.statSync(itemPath);
          return `${stats.isDirectory() ? 'DIR' : 'FILE'}: ${item}`;
        }).join('\n');
      }
      return `Directory not found: ${dirPath}`;
    } catch (error) {
      // Fallback to in-memory
      if (this.directories[dirPath]) {
        return this.directories[dirPath].join('\n');
      }
      return `Directory not found: ${dirPath}`;
    }
  }

  createDirectory(dirName) {
    try {
      const fullPath = path.join(this.basePath, dirName);
      fs.mkdirSync(fullPath, { recursive: true });
      return `Directory created: ${dirName}`;
    } catch (error) {
      // Fallback to in-memory
      this.directories[dirName] = [];
      return `Directory created: ${dirName}`;
    }
  }

  writeFile(fileName, content) {
    try {
      const fullPath = path.join(this.basePath, fileName);
      fs.writeFileSync(fullPath, content);
      return `File written: ${fileName}`;
    } catch (error) {
      // Fallback to in-memory
      this.files[fileName] = content;
      return `File written: ${fileName}`;
    }
  }

  readFile(fileName) {
    try {
      const fullPath = path.join(this.basePath, fileName);
      if (fs.existsSync(fullPath)) {
        return fs.readFileSync(fullPath, 'utf8');
      }
      return `File not found: ${fileName}`;
    } catch (error) {
      // Fallback to in-memory
      if (this.files[fileName]) {
        return this.files[fileName];
      }
      return `File not found: ${fileName}`;
    }
  }
}

// Terminal Implementation
class Terminal {
  constructor() {
    this.history = [];
    this.currentSession = [];
  }

  clear() {
    this.currentSession = [];
    return 'Terminal cleared';
  }

  addToHistory(command, output) {
    this.history.push({ command, output, timestamp: Date.now() });
    this.currentSession.push({ command, output, timestamp: Date.now() });
  }

  getSessionOutput() {
    return this.currentSession;
  }
}

// AI Interface Implementation
class AIInterface {
  constructor() {
    this.model = 'jaegis-ai-v1';
    this.context = [];
  }

  async processQuery(query) {
    // Simulate AI processing
    const responses = {
      'hello': 'Hello! I am JAEGIS-OS AI assistant. How can I help you?',
      'help': 'I can help you with system operations, file management, and answer questions about JAEGIS-OS.',
      'status': 'All systems operational. AI interface is running normally.',
      'default': `Processing your query: "${query}". This is a simulated AI response.`
    };

    const lowerQuery = query.toLowerCase();
    let response = responses.default;

    for (const [key, value] of Object.entries(responses)) {
      if (lowerQuery.includes(key)) {
        response = value;
        break;
      }
    }

    // Add to context
    this.context.push({ role: 'user', content: query });
    this.context.push({ role: 'assistant', content: response });

    return response;
  }
}

// Web Server Implementation
class JAEGISServer {
  constructor(port = process.env.PORT || 3000) {
    this.port = port;
    this.core = new JAEGISCore();
    this.server = null;
  }

  start() {
    this.server = http.createServer((req, res) => {
      this.handleRequest(req, res);
    });

    this.server.listen(this.port, () => {
      console.log(`JAEGIS-OS Server running on port ${this.port}`);
      console.log(`Access your JAEGIS-OS at: http://localhost:${this.port}`);
    });
  }

  handleRequest(req, res) {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;

    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
      res.writeHead(200);
      res.end();
      return;
    }

    switch (pathname) {
      case '/':
        this.serveIndex(res);
        break;
      case '/api/command':
        this.handleCommand(req, res);
        break;
      case '/api/status':
        this.handleStatus(req, res);
        break;
      case '/api/ai':
        this.handleAIRequest(req, res);
        break;
      case '/api/files':
        this.handleFileRequest(req, res);
        break;
      default:
        this.serveStatic(req, res, pathname);
        break;
    }
  }

  serveIndex(res) {
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JAEGIS-OS - AI Powered Operating System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            height: 100vh;
            overflow: hidden;
        }

        .container {
            display: grid;
            grid-template-rows: 60px 1fr 120px;
            height: 100vh;
        }

        .header {
            background: #1a1a1a;
            border-bottom: 2px solid #00ff00;
            display: flex;
            align-items: center;
            padding: 0 20px;
        }

        .header h1 {
            font-size: 24px;
            color: #00ff00;
        }

        .status {
            margin-left: auto;
            font-size: 14px;
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2px;
            background: #333;
        }

        .terminal, .ai-panel {
            background: #0a0a0a;
            padding: 20px;
            overflow-y: auto;
        }

        .terminal h3, .ai-panel h3 {
            color: #00ff00;
            margin-bottom: 10px;
            border-bottom: 1px solid #00ff00;
            padding-bottom: 5px;
        }

        .output {
            white-space: pre-wrap;
            font-size: 14px;
            line-height: 1.4;
        }

        .input-area {
            background: #1a1a1a;
            border-top: 2px solid #00ff00;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .input-row {
            display: flex;
            gap: 10px;
        }

        input[type="text"] {
            flex: 1;
            background: #0a0a0a;
            border: 1px solid #00ff00;
            color: #00ff00;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }

        button {
            background: #00ff00;
            color: #0a0a0a;
            border: none;
            padding: 10px 20px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #00cc00;
        }

        .tab-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }

        .tab-button {
            background: #333;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 5px 15px;
            cursor: pointer;
        }

        .tab-button.active {
            background: #00ff00;
            color: #0a0a0a;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>JAEGIS-OS</h1>
            <div class="status" id="systemStatus">System: Online</div>
        </div>

        <div class="main-content">
            <div class="terminal">
                <h3>Terminal</h3>
                <div class="output" id="terminalOutput">JAEGIS-OS Terminal v1.0
Type 'help' for available commands.
</div>
            </div>

            <div class="ai-panel">
                <div class="tab-buttons">
                    <div class="tab-button active" onclick="switchTab('ai')">AI Chat</div>
                    <div class="tab-button" onclick="switchTab('files')">Files</div>
                    <div class="tab-button" onclick="switchTab('status')">Status</div>
                </div>

                <div id="ai-tab" class="tab-content active">
                    <h3>AI Assistant</h3>
                    <div class="output" id="aiOutput">Hello! I'm JAEGIS-OS AI assistant. How can I help you today?</div>
                </div>

                <div id="files-tab" class="tab-content">
                    <h3>File System</h3>
                    <div class="output" id="filesOutput">File system ready. Use terminal commands to manage files.</div>
                </div>

                <div id="status-tab" class="tab-content">
                    <h3>System Status</h3>
                    <div class="output" id="statusOutput">Loading system status...</div>
                </div>
            </div>
        </div>

        <div class="input-area">
            <div class="input-row">
                <input type="text" id="commandInput" placeholder="Enter command or AI query..." onkeypress="handleKeyPress(event)">
                <button onclick="executeCommand()">Execute</button>
                <button onclick="clearTerminal()">Clear</button>
            </div>
            <div style="font-size: 12px; color: #666;">
                Commands: help, status, ls, mkdir, write, read, ai [query], clear
            </div>
        </div>
    </div>

    <script>
        let currentTab = 'ai';

        function switchTab(tab) {
            currentTab = tab;
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            document.querySelector(\`[onclick="switchTab('\${tab}')"]\`).classList.add('active');
            document.getElementById(\`\${tab}-tab\`).classList.add('active');

            if (tab === 'status') {
                updateSystemStatus();
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                executeCommand();
            }
        }

        async function executeCommand() {
            const input = document.getElementById('commandInput');
            const command = input.value.trim();
            
            if (!command) return;

            // Add to terminal output
            const terminalOutput = document.getElementById('terminalOutput');
            terminalOutput.textContent += \`\\n> \${command}\`;

            try {
                let response;
                if (command.startsWith('ai ')) {
                    response = await fetch('/api/ai', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query: command.substring(3) })
                    });
                    const data = await response.json();
                    response = data.response;
                } else {
                    response = await fetch('/api/command', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ command, args: [] })
                    });
                    const data = await response.json();
                    response = data.output;
                }

                terminalOutput.textContent += \`\\n\${response}\`;
                terminalOutput.scrollTop = terminalOutput.scrollHeight;

                // Update relevant panels
                if (command.startsWith('ai ')) {
                    document.getElementById('aiOutput').textContent = response;
                } else if (command === 'status') {
                    document.getElementById('statusOutput').textContent = response;
                } else if (command.startsWith('ls') || command.startsWith('mkdir') || command.startsWith('write') || command.startsWith('read')) {
                    document.getElementById('filesOutput').textContent = response;
                }

            } catch (error) {
                terminalOutput.textContent += \`\\nError: \${error.message}\`;
            }

            input.value = '';
        }

        function clearTerminal() {
            document.getElementById('terminalOutput').textContent = 'JAEGIS-OS Terminal v1.0\\nType \\'help\\' for available commands.\\n';
        }

        async function updateSystemStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                document.getElementById('statusOutput').textContent = data.status;
                document.getElementById('systemStatus').textContent = \`System: \${data.running ? 'Online' : 'Offline'}\`;
            } catch (error) {
                document.getElementById('statusOutput').textContent = 'Error fetching status';
            }
        }

        // Initialize
        updateSystemStatus();
        setInterval(updateSystemStatus, 30000); // Update every 30 seconds
    </script>
</body>
</html>`;

    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(html);
  }

  async handleCommand(req, res) {
    if (req.method !== 'POST') {
      res.writeHead(405, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Method not allowed' }));
      return;
    }

    try {
      const body = await this.getRequestBody(req);
      const { command, args } = JSON.parse(body);
      const output = await this.core.executeCommand(command, args);
      
      this.core.terminal.addToHistory(command, output);
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ output }));
    } catch (error) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: error.message }));
    }
  }

  async handleStatus(req, res) {
    const status = this.core.getStatus();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ 
      status,
      running: this.core.systemStatus.running,
      uptime: Date.now() - this.core.systemStatus.uptime
    }));
  }

  async handleAIRequest(req, res) {
    if (req.method !== 'POST') {
      res.writeHead(405, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Method not allowed' }));
      return;
    }

    try {
      const body = await this.getRequestBody(req);
      const { query } = JSON.parse(body);
      const response = await this.core.ai.processQuery(query);
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ response }));
    } catch (error) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: error.message }));
    }
  }

  async handleFileRequest(req, res) {
    const files = this.core.fileSystem.listFiles('/');
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ files }));
  }

  serveStatic(req, res, pathname) {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not found');
  }

  getRequestBody(req) {
    return new Promise((resolve, reject) => {
      let body = '';
      req.on('data', chunk => {
        body += chunk.toString();
      });
      req.on('end', () => {
        resolve(body);
      });
      req.on('error', reject);
    });
  }
}

// Command Line Interface
function handleCommandLine() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
JAEGIS-OS - AI Powered Operating System
=======================================

Usage:
  node jaegis-os-complete.js              # Start server
  node jaegis-os-complete.js --help      # Show this help

Commands:
  help              - Show available commands
  status            - Show system status
  ls [path]         - List files
  mkdir <name>      - Create directory
  write <file> <content> - Write file
  read <file>       - Read file
  ai <query>        - Ask AI assistant
  clear             - Clear terminal

Features:
  • Terminal interface
  • AI Assistant
  • File system
  • System monitoring
  • Web interface
  • HTTPS security
  • Free hosting support
`);
    process.exit(0);
  }

  // Start the server
  const port = process.env.PORT || 3000;
  const server = new JAEGISServer(port);
  server.start();
}

// Start the application
if (require.main === module) {
  handleCommandLine();
}

module.exports = { JAEGISServer, JAEGISCore };