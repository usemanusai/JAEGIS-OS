#!/usr/bin/env node

const http = require('http');
const url = require('url');

class JAEGISCore {
  constructor() {
    this.systemStatus = {
      running: true,
      uptime: Date.now(),
      memory: { used: 45, total: 100 },
      cpu: { usage: 12 },
      processes: [
        { name: 'N.L.D.S. Terminal', status: 'active', cpu: 8 },
        { name: 'Forge Console', status: 'active', cpu: 15 },
        { name: 'AI Assistant', status: 'active', cpu: 5 },
        { name: 'File System', status: 'active', cpu: 3 },
        { name: 'System Monitor', status: 'active', cpu: 2 }
      ]
    };
    this.files = {};
    this.directories = { '/': [] };
  }

  async executeCommand(command, args = []) {
    switch(command.toLowerCase()) {
      case 'help': return this.showHelp();
      case 'status': return this.getStatus();
      case 'apps': return this.listApps();
      case 'launch': return this.launchApp(args[0]);
      case 'ls': return this.listFiles(args[0] || '/');
      case 'mkdir': return this.createDirectory(args[0]);
      case 'write': return this.writeFile(args[0], args.slice(1).join(' '));
      case 'read': return this.readFile(args[0]);
      case 'ai': return this.processAI(args.join(' '));
      case 'clear': return 'Terminal cleared';
      case 'squad': return this.squadStatus();
      case 'research': return this.initiateResearch(args.join(' '));
      default: return `Unknown command: ${command}. Type 'help' for commands.`;
    }
  }

  showHelp() {
    return `JAEGIS-OS COMMANDS:
==================
SYSTEM: help, status, apps, launch <app>
TERMINAL: clear
FILE SYSTEM: ls, mkdir, write, read
AI & RESEARCH: ai <query>, squad, research <topic>

EXAMPLES: launch nlds-terminal, ai Hello, research AI`;
  }

  getStatus() {
    const uptime = Math.floor((Date.now() - this.systemStatus.uptime) / 1000);
    return `JAEGIS-OS STATUS:
Running: ${this.systemStatus.running}
Uptime: ${uptime}s
Memory: ${this.systemStatus.memory.used}MB/${this.systemStatus.memory.total}MB
CPU: ${this.systemStatus.cpu.usage}%
Processes: ${this.systemStatus.processes.length}`;
  }

  listApps() {
    return `AVAILABLE APPS:
🧠 N.L.D.S. Terminal     - Advanced Research
⚒️ Forge Console         - Squad Management  
🎯 JAEGIS Core           - System Control
🚀 Deployment Center     - App Deployment
💬 AI Chat              - Conversational AI
🔍 AI Search            - Intelligent Search
🤖 LLM-OS Integration   - Language Model Ops
🧠 Hive Mind            - Collaborative AI
⚙️ System Admin         - System Admin
🔧 Settings             - Configuration

USAGE: launch <app-name>`;
  }

  launchApp(appName) {
    const apps = {
      'nlds-terminal': '🧠 N.L.D.S. Terminal launched - Research System Online',
      'forge-console': '⚒️ Forge Console launched - Squad Management Active',
      'core': '🎯 JAEGIS Core launched - Control Center Online',
      'deployment': '🚀 Deployment Center launched - Deployment Ready',
      'ai-chat': '💬 AI Chat launched - Chat Interface Ready',
      'ai-search': '🔍 AI Search launched - Search System Online',
      'llm-os': '🤖 LLM-OS Integration launched - Language Model Ops Active',
      'hive-mind': '🧠 Hive Mind launched - Collaborative AI Online',
      'system-admin': '⚙️ System Admin launched - Admin Interface Ready',
      'settings': '🔧 Settings launched - Config Interface Open'
    };

    const appKey = appName.toLowerCase().replace(/\s+/g, '-');
    return apps[appKey] || `❌ App not found: ${appName}. Type 'apps' to see available apps.`;
  }

  listFiles(dirPath = '/') {
    if (this.directories[dirPath]) {
      return this.directories[dirPath].map(file => `FILE: ${file}`).join('\n');
    }
    return `Directory not found: ${dirPath}`;
  }

  createDirectory(dirName) {
    this.directories[dirName] = [];
    if (!this.directories['/'].includes(dirName)) {
      this.directories['/'].push(dirName);
    }
    return `Directory created: ${dirName}`;
  }

  writeFile(fileName, content) {
    this.files[fileName] = content;
    if (!this.directories['/'].includes(fileName)) {
      this.directories['/'].push(fileName);
    }
    return `File written: ${fileName}`;
  }

  readFile(fileName) {
    return this.files[fileName] || `File not found: ${fileName}`;
  }

  processAI(query) {
    const responses = {
      'hello': 'Hello! I am JAEGIS-OS AI assistant. I can help with system operations, research, and answer questions.',
      'help': 'I can assist with system commands, app launching, file management, research coordination, and technical support.',
      'status': 'All JAEGIS-OS systems are operational. AI interface running normally with full system access.',
      'what is jaegis': 'JAEGIS-OS is an AI-Powered Operating System with multi-agent research, squad management, and various integrated applications.',
      'default': `Processing: "${query}". Analyzing your request based on JAEGIS-OS capabilities.`
    };

    const lowerQuery = query.toLowerCase();
    let response = responses.default;
    for (const [key, value] of Object.entries(responses)) {
      if (lowerQuery.includes(key)) {
        response = value;
        break;
      }
    }
    return response;
  }

  squadStatus() {
    return `SQUAD STATUS:
==============
🔥 Alpha Squad: ACTIVE (5 agents)
   • Lead Researcher: ONLINE
   • Data Analyst: ONLINE  
   • Knowledge Synthesizer: ONLINE
   • Web Search Specialist: ONLINE
   • Validation Agent: ONLINE

⚡ Beta Squad: ACTIVE (4 agents)
   • Task Manager: ONLINE
   • Coordinator: ONLINE
   • Security Specialist: ONLINE
   • Communications: ONLINE

🛡️ Gamma Squad: STANDBY (3 agents)
   • System Monitor: ONLINE
   • Backup Specialist: ONLINE
   • Recovery Agent: ONLINE

🌊 Delta Squad: ACTIVE (6 agents)
   • Research Lead: ONLINE
   • Data Processor: ONLINE
   • AI Specialist: ONLINE
   • Quality Assurance: ONLINE

TOTAL AGENTS: 18 | ACTIVE SQUADS: 3 | SUCCESS RATE: 94%`;
  }

  initiateResearch(topic) {
    if (!topic) return '❌ Specify research topic. Usage: research <topic>';
    return `🔬 RESEARCH INITIATED: ${topic.toUpperCase()}
========================================
Deploying research squads...
Initializing data collection...
Setting up analysis pipelines...

RESEARCH PROTOCOLS: Multi-agent analysis, Web crawling, Data processing, Knowledge synthesis
ESTIMATED COMPLETION: 3-5 minutes
RESEARCH SQUADS: 2 deployed
Status: Research in progress...`;
  }
}

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  const pathname = url.parse(req.url).pathname;

  if (pathname === '/') {
    const html = `<!DOCTYPE html>
<html>
<head>
    <title>JAEGIS-OS - AI Powered Operating System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #00ff88; 
            height: 100vh; 
            overflow: hidden; 
        }
        .container { display: grid; grid-template-rows: 60px 1fr 140px; height: 100vh; }
        .header { 
            background: rgba(0, 255, 136, 0.1); 
            border-bottom: 2px solid #00ff88; 
            display: flex; 
            align-items: center; 
            padding: 0 20px; 
            backdrop-filter: blur(10px); 
        }
        .header h1 { font-size: 24px; color: #00ff88; text-shadow: 0 0 10px rgba(0, 255, 136, 0.5); }
        .status { margin-left: auto; font-size: 14px; display: flex; align-items: center; gap: 10px; }
        .status-indicator { 
            width: 8px; height: 8px; background: #00ff88; border-radius: 50%; 
            animation: pulse 2s infinite; 
        }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        .main-content { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 2px; 
            background: rgba(0, 255, 136, 0.1); 
        }
        .terminal, .app-panel { 
            background: rgba(0, 0, 0, 0.8); 
            padding: 20px; 
            overflow-y: auto; 
            backdrop-filter: blur(5px); 
        }
        .terminal h3, .app-panel h3 { 
            color: #00ff88; 
            margin-bottom: 15px; 
            border-bottom: 1px solid #00ff88; 
            padding-bottom: 8px; 
            font-size: 16px; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
        }
        .output { 
            white-space: pre-wrap; 
            font-size: 13px; 
            line-height: 1.5; 
            font-family: 'Courier New', monospace; 
            color: #00ff88; 
        }
        .input-area { 
            background: rgba(0, 255, 136, 0.05); 
            border-top: 2px solid #00ff88; 
            padding: 20px; 
            display: flex; 
            flex-direction: column; 
            gap: 15px; 
        }
        .input-row { display: flex; gap: 10px; }
        input[type="text"] { 
            flex: 1; 
            background: rgba(0, 0, 0, 0.8); 
            border: 1px solid #00ff88; 
            color: #00ff88; 
            padding: 12px; 
            font-family: 'Courier New', monospace; 
            font-size: 14px; 
            border-radius: 4px; 
            outline: none; 
        }
        input[type="text"]:focus { box-shadow: 0 0 10px rgba(0, 255, 136, 0.3); }
        button { 
            background: linear-gradient(45deg, #00ff88, #00cc6a); 
            color: #000; 
            border: none; 
            padding: 12px 20px; 
            font-family: 'Courier New', monospace; 
            font-weight: bold; 
            cursor: pointer; 
            border-radius: 4px; 
            transition: all 0.3s ease; 
        }
        button:hover { 
            background: linear-gradient(45deg, #00cc6a, #00ff88); 
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.4); 
        }
        .tab-buttons { display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap; }
        .tab-button { 
            background: rgba(0, 255, 136, 0.1); 
            color: #00ff88; 
            border: 1px solid #00ff88; 
            padding: 8px 16px; 
            cursor: pointer; 
            border-radius: 4px; 
            font-size: 12px; 
            transition: all 0.3s ease; 
            text-transform: uppercase; 
            letter-spacing: 0.5px; 
        }
        .tab-button:hover { background: rgba(0, 255, 136, 0.2); }
        .tab-button.active { 
            background: linear-gradient(45deg, #00ff88, #00cc6a); 
            color: #000; 
            border-color: #00ff88; 
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .quick-actions { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
        .quick-btn { 
            background: rgba(0, 255, 136, 0.1); 
            color: #00ff88; 
            border: 1px solid #00ff88; 
            padding: 6px 12px; 
            font-size: 11px; 
            border-radius: 3px; 
            cursor: pointer; 
            transition: all 0.3s ease; 
        }
        .quick-btn:hover { background: rgba(0, 255, 136, 0.2); }
        .system-info { 
            font-size: 11px; 
            color: rgba(0, 255, 136, 0.7); 
            margin-top: 10px; 
        }
        @media (max-width: 768px) {
            .main-content { grid-template-columns: 1fr; }
            .header h1 { font-size: 18px; }
            .input-row { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 JAEGIS-OS</h1>
            <div class="status">
                <div class="status-indicator"></div>
                <span id="systemStatus">System: Online</span>
            </div>
        </div>

        <div class="main-content">
            <div class="terminal">
                <h3>🖥️ Terminal</h3>
                <div class="output" id="terminalOutput">🚀 JAEGIS-OS Terminal v1.0
AI-Powered Operating System Online
Type 'help' for available commands.

> system initialized
> all services operational
> ready for commands

</div>
            </div>

            <div class="app-panel">
                <div class="tab-buttons">
                    <div class="tab-button active" onclick="switchTab('apps')">📱 Apps</div>
                    <div class="tab-button" onclick="switchTab('ai')">🤖 AI Chat</div>
                    <div class="tab-button" onclick="switchTab('files')">📁 Files</div>
                    <div class="tab-button" onclick="switchTab('status')">📊 Status</div>
                    <div class="tab-button" onclick="switchTab('squad')">👥 Squad</div>
                </div>

                <div id="apps-tab" class="tab-content active">
                    <h3>📱 Applications</h3>
                    <div class="output" id="appsOutput">🧠 N.L.D.S. Terminal     - Advanced Research System
⚒️ Forge Console         - Squad Management  
🎯 JAEGIS Core           - System Control Center
🚀 Deployment Center     - Application Deployment
💬 AI Chat              - Conversational AI
🔍 AI Search            - Intelligent Search
🤖 LLM-OS Integration   - Language Model Operations
🧠 Hive Mind            - Collaborative AI System
⚙️ System Admin         - System Administration
🔧 Settings             - Configuration Management

Type 'launch <app-name>' to start an application</div>
                    <div class="quick-actions">
                        <div class="quick-btn" onclick="quickLaunch('nlds-terminal')">🧠 Terminal</div>
                        <div class="quick-btn" onclick="quickLaunch('ai-chat')">💬 AI Chat</div>
                        <div class="quick-btn" onclick="quickLaunch('forge-console')">⚒️ Console</div>
                        <div class="quick-btn" onclick="quickLaunch('core')">🎯 Core</div>
                    </div>
                </div>

                <div id="ai-tab" class="tab-content">
                    <h3>🤖 AI Assistant</h3>
                    <div class="output" id="aiOutput">Hello! I'm JAEGIS-OS AI assistant. I can help you with system operations, research coordination, file management, and answer questions about JAEGIS-OS capabilities.

How can I assist you today?</div>
                </div>

                <div id="files-tab" class="tab-content">
                    <h3>📁 File System</h3>
                    <div class="output" id="filesOutput">Virtual File System ready.
Use 'ls' to list files, 'mkdir <name>' to create directories, 'write <file> <content>' to write files.</div>
                </div>

                <div id="status-tab" class="tab-content">
                    <h3>📊 System Status</h3>
                    <div class="output" id="statusOutput">Loading system status...</div>
                </div>

                <div id="squad-tab" class="tab-content">
                    <h3>👥 Squad Management</h3>
                    <div class="output" id="squadOutput">Loading squad status...</div>
                </div>
            </div>
        </div>

        <div class="input-area">
            <div class="input-row">
                <input type="text" id="commandInput" placeholder="Enter command or AI query..." onkeypress="handleKeyPress(event)">
                <button onclick="executeCommand()">Execute</button>
                <button onclick="clearTerminal()">Clear</button>
            </div>
            <div style="font-size: 12px; color: rgba(0, 255, 136, 0.6);">
                💡 Quick Commands: help, status, apps, launch <app>, ai <query>, ls, squad, research <topic>
            </div>
            <div class="system-info">
                🚀 JAEGIS-OS v1.0 | AI-Powered Operating System | Free HTTPS Hosting | Multi-Agent System
            </div>
        </div>
    </div>

    <script>
        let currentTab = 'apps';

        function switchTab(tab) {
            currentTab = tab;
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            document.querySelector(\`[onclick="switchTab('\${tab}')"]\`).classList.add('active');
            document.getElementById(\`\${tab}-tab\`).classList.add('active');

            if (tab === 'status') updateSystemStatus();
            else if (tab === 'squad') updateSquadStatus();
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') executeCommand();
        }

        async function executeCommand() {
            const input = document.getElementById('commandInput');
            const command = input.value.trim();
            if (!command) return;

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

                if (command.startsWith('ai ')) {
                    document.getElementById('aiOutput').textContent = response;
                } else if (command === 'status') {
                    document.getElementById('statusOutput').textContent = response;
                } else if (command === 'apps') {
                    document.getElementById('appsOutput').textContent = response;
                } else if (command.startsWith('launch')) {
                    document.getElementById('appsOutput').textContent = response;
                } else if (command === 'squad') {
                    document.getElementById('squadOutput').textContent = response;
                } else if (command.startsWith('research')) {
                    document.getElementById('squadOutput').textContent = response;
                } else if (['ls', 'mkdir', 'write', 'read'].some(cmd => command.startsWith(cmd))) {
                    updateFileList();
                }

            } catch (error) {
                terminalOutput.textContent += \`\\nError: \${error.message}\`;
            }

            input.value = '';
        }

        function clearTerminal() {
            document.getElementById('terminalOutput').textContent = '🚀 JAEGIS-OS Terminal v1.0\\nAI-Powered Operating System Online\\nType \\'help\\' for available commands.\\n\\n> system initialized\\n> all services operational\\n> ready for commands\\n\\n';
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

        async function updateSquadStatus() {
            try {
                const response = await fetch('/api/command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command: 'squad', args: [] })
                });
                const data = await response.json();
                document.getElementById('squadOutput').textContent = data.output;
            } catch (error) {
                document.getElementById('squadOutput').textContent = 'Error fetching squad status';
            }
        }

        async function updateFileList() {
            try {
                const response = await fetch('/api/files');
                const data = await response.json();
                document.getElementById('filesOutput').textContent = data.files;
            } catch (error) {
                document.getElementById('filesOutput').textContent = 'Error fetching file list';
            }
        }

        async function quickLaunch(appName) {
            const command = \`launch \${appName}\`;
            const input = document.getElementById('commandInput');
            input.value = command;
            executeCommand();
        }

        updateSystemStatus();
        setInterval(updateSystemStatus, 30000);
    </script>
</body>
</html>`;

    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(html);
    return;
  }

  if (pathname === '/api/command' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk.toString());
    req.on('end', () => {
      try {
        const { command, args } = JSON.parse(body);
        const core = new JAEGISCore();
        core.executeCommand(command, args).then(output => {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ output }));
        });
      } catch (error) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: error.message }));
      }
    });
    return;
  }

  if (pathname === '/api/ai' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk.toString());
    req.on('end', () => {
      try {
        const { query } = JSON.parse(body);
        const core = new JAEGISCore();
        const response = core.processAI(query);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ response }));
      } catch (error) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: error.message }));
      }
    });
    return;
  }

  if (pathname === '/api/status') {
    const core = new JAEGISCore();
    const status = core.getStatus();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status, running: true }));
    return;
  }

  if (pathname === '/api/files') {
    const core = new JAEGISCore();
    const files = core.listFiles('/');
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ files }));
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('Not found');
});

const port = process.env.PORT || 3000;
server.listen(port, () => {
  console.log(`🚀 JAEGIS-OS Server running on port ${port}`);
});
