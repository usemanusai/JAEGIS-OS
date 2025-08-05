// AppRegistry.js - Application Registry and Management
import { WebOSAppContainer } from './AppFramework';

// Application Registry
class AppRegistry {
  constructor() {
    this.registeredApps = new Map();
    this.runningApps = new Map();
    this.appCategories = new Map();
    this.windowManager = null;
    this.initialized = false;
  }
  
  // Initialize the registry
  async initialize(windowManager) {
    this.windowManager = windowManager;
    await this.registerDefaultApps();
    this.initialized = true;
    console.log('✅ App Registry initialized');
  }
  
  // Register application
  registerApp(appConfig) {
    const appContainer = new WebOSAppContainer(appConfig);
    this.registeredApps.set(appConfig.id, appContainer);
    
    // Categorize app
    const category = appConfig.category || 'General';
    if (!this.appCategories.has(category)) {
      this.appCategories.set(category, []);
    }
    this.appCategories.get(category).push(appConfig.id);
    
    console.log(`📱 Registered app: ${appConfig.name}`);
  }
  
  // Launch application
  async launchApp(appId, windowConfig = {}) {
    const appContainer = this.registeredApps.get(appId);
    if (!appContainer) {
      throw new Error(`App not found: ${appId}`);
    }
    
    // Initialize container if not already done
    if (!appContainer.initialized) {
      await appContainer.initialize();
    }
    
    // Create window for app
    const windowId = await this.createAppWindow(appContainer, windowConfig);
    
    // Track running app
    this.runningApps.set(windowId, appContainer);
    
    return windowId;
  }
  
  // Create application window
  async createAppWindow(appContainer, windowConfig) {
    if (!this.windowManager) {
      throw new Error('Window manager not initialized');
    }
    
    const defaultConfig = {
      title: appContainer.appName,
      component: appContainer.component,
      props: appContainer.getAppProps(),
      icon: appContainer.appConfig.icon,
      defaultSize: appContainer.appConfig.defaultSize || { width: 800, height: 600 },
      minSize: appContainer.appConfig.minSize || { width: 400, height: 300 },
      resizable: appContainer.appConfig.resizable !== false,
      maximizable: appContainer.appConfig.maximizable !== false,
      minimizable: appContainer.appConfig.minimizable !== false
    };
    
    const finalConfig = { ...defaultConfig, ...windowConfig };
    const windowId = await this.windowManager.createWindow(finalConfig);
    
    return windowId;
  }
  
  // Get registered applications
  getRegisteredApps() {
    return Array.from(this.registeredApps.values()).map(container => ({
      id: container.appId,
      name: container.appName,
      type: container.appType,
      category: container.appConfig.category,
      icon: container.appConfig.icon,
      description: container.appConfig.description
    }));
  }
  
  // Get applications by category
  getAppsByCategory(category) {
    const appIds = this.appCategories.get(category) || [];
    return appIds.map(id => this.registeredApps.get(id)).filter(Boolean);
  }
  
  // Get all categories
  getCategories() {
    return Array.from(this.appCategories.keys());
  }
  
  // Register default JAEGIS applications
  async registerDefaultApps() {
    // JAEGIS Core Application
    this.registerApp({
      id: 'jaegis-core',
      name: 'JAEGIS Core',
      type: 'react',
      category: 'Management',
      icon: '/icons/jaegis-core.svg',
      description: 'JAEGIS Core Management Interface',
      defaultSize: { width: 1000, height: 700 },
      permissions: ['system_access', 'agent_management'],
      security: {
        permissions: ['system_access', 'agent_management'],
        isolationLevel: 'standard'
      }
    });
    
    // N.L.D.S. Terminal
    this.registerApp({
      id: 'nlds-terminal',
      name: 'N.L.D.S. Terminal',
      type: 'react',
      category: 'Research',
      icon: '/icons/terminal.svg',
      description: 'Natural Language Data Science Terminal',
      defaultSize: { width: 900, height: 600 },
      permissions: ['nlds_access', 'data_processing'],
      security: {
        permissions: ['nlds_access', 'data_processing'],
        isolationLevel: 'high'
      }
    });
    
    // LLM OS
    this.registerApp({
      id: 'llm-os',
      name: 'LLM OS',
      type: 'react',
      category: 'AI',
      icon: '/icons/llm-os.svg',
      description: 'Large Language Model Operating System',
      defaultSize: { width: 1200, height: 800 },
      permissions: ['llm_access', 'ai_processing'],
      security: {
        permissions: ['llm_access', 'ai_processing'],
        isolationLevel: 'high'
      }
    });
    
    // AI Chat
    this.registerApp({
      id: 'ai-chat',
      name: 'AI Chat',
      type: 'react',
      category: 'AI',
      icon: '/icons/chat.svg',
      description: 'AI-powered Chat Interface',
      defaultSize: { width: 800, height: 600 },
      permissions: ['ai_chat', 'conversation_history'],
      security: {
        permissions: ['ai_chat', 'conversation_history'],
        isolationLevel: 'standard'
      }
    });
    
    // AI Search
    this.registerApp({
      id: 'ai-search',
      name: 'AI Search',
      type: 'react',
      category: 'AI',
      icon: '/icons/search.svg',
      description: 'Intelligent Search Interface',
      defaultSize: { width: 900, height: 700 },
      permissions: ['search_access', 'data_indexing'],
      security: {
        permissions: ['search_access', 'data_indexing'],
        isolationLevel: 'standard'
      }
    });
    
    // Deployment Center
    this.registerApp({
      id: 'deployment-center',
      name: 'Deployment Center',
      type: 'react',
      category: 'Development',
      icon: '/icons/deployment.svg',
      description: 'Application Deployment Management',
      defaultSize: { width: 1100, height: 800 },
      permissions: ['deployment_access', 'system_config'],
      security: {
        permissions: ['deployment_access', 'system_config'],
        isolationLevel: 'high'
      }
    });
    
    // Forge Console
    this.registerApp({
      id: 'forge-console',
      name: 'Forge Console',
      type: 'react',
      category: 'Management',
      icon: '/icons/forge.svg',
      description: 'Tool Forging and Management Console',
      defaultSize: { width: 1000, height: 700 },
      permissions: ['forge_access', 'tool_management'],
      security: {
        permissions: ['forge_access', 'tool_management'],
        isolationLevel: 'high'
      }
    });
    
    // JAEGIS Cockpit (Iframe Integration)
    this.registerApp({
      id: 'jaegis-cockpit',
      name: 'JAEGIS Cockpit',
      type: 'iframe',
      category: 'System',
      icon: '/icons/cockpit.svg',
      description: 'JAEGIS System Control Interface',
      url: 'http://localhost:8090',
      defaultSize: { width: 1200, height: 800 },
      minSize: { width: 800, height: 600 },
      permissions: ['system_access', 'agent_management'],
      security: {
        permissions: ['system_access', 'agent_management'],
        isolationLevel: 'standard'
      }
    });
    
    // Text Editor
    this.registerApp({
      id: 'text-editor',
      name: 'Text Editor',
      type: 'react',
      category: 'Development',
      icon: '/icons/text-editor.svg',
      description: 'Advanced Text Editor with AI assistance',
      defaultSize: { width: 900, height: 600 },
      permissions: ['file_access', 'ai_assistance'],
      security: {
        permissions: ['file_access', 'ai_assistance'],
        isolationLevel: 'standard'
      }
    });
    
    // File Explorer
    this.registerApp({
      id: 'file-explorer',
      name: 'File Explorer',
      type: 'react',
      category: 'System',
      icon: '/icons/folder.svg',
      description: 'File System Browser and Manager',
      defaultSize: { width: 800, height: 600 },
      permissions: ['file_system_access', 'file_operations'],
      security: {
        permissions: ['file_system_access', 'file_operations'],
        isolationLevel: 'standard'
      }
    });
    
    // Terminal
    this.registerApp({
      id: 'terminal',
      name: 'Terminal',
      type: 'react',
      category: 'Development',
      icon: '/icons/terminal.svg',
      description: 'System Terminal with AI enhancement',
      defaultSize: { width: 800, height: 500 },
      permissions: ['system_access', 'command_execution'],
      security: {
        permissions: ['system_access', 'command_execution'],
        isolationLevel: 'high'
      }
    });
    
    // System Info
    this.registerApp({
      id: 'system-info',
      name: 'System Info',
      type: 'react',
      category: 'System',
      icon: '/icons/info.svg',
      description: 'System Information and Monitoring',
      defaultSize: { width: 700, height: 500 },
      permissions: ['system_monitoring', 'performance_data'],
      security: {
        permissions: ['system_monitoring', 'performance_data'],
        isolationLevel: 'standard'
      }
    });

    // Agent Coordination Dashboard
    this.registerApp({
      id: 'agent-coordination',
      name: 'Agent Coordination',
      type: 'react',
      category: 'Management',
      icon: '/icons/agents.svg',
      description: '7-Tier Agent Hierarchy Visualization and Coordination',
      defaultSize: { width: 1200, height: 800 },
      permissions: ['agent_management', 'system_monitoring'],
      security: {
        permissions: ['agent_management', 'system_monitoring'],
        isolationLevel: 'standard'
      }
    });

    // Real-time Monitoring Dashboard
    this.registerApp({
      id: 'monitoring-dashboard',
      name: 'Monitoring Dashboard',
      type: 'react',
      category: 'System',
      icon: '/icons/monitoring.svg',
      description: 'Real-time System Performance and Health Monitoring',
      defaultSize: { width: 1400, height: 900 },
      permissions: ['system_monitoring', 'performance_data'],
      security: {
        permissions: ['system_monitoring', 'performance_data'],
        isolationLevel: 'standard'
      }
    });
  }
  
  // Close application
  closeApp(windowId) {
    const appContainer = this.runningApps.get(windowId);
    if (appContainer) {
      // Perform cleanup
      this.runningApps.delete(windowId);
      console.log(`📱 Closed app: ${appContainer.appName}`);
    }
  }
  
  // Get running applications
  getRunningApps() {
    return Array.from(this.runningApps.entries()).map(([windowId, container]) => ({
      windowId,
      appId: container.appId,
      appName: container.appName
    }));
  }
}

// Global app registry instance
export const appRegistry = new AppRegistry();
export default AppRegistry;
