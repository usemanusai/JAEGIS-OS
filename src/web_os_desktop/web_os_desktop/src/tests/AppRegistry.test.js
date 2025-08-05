// AppRegistry.test.js - Tests for Application Registry
import AppRegistry from '../services/AppRegistry';
import { WebOSAppContainer } from '../services/AppFramework';

// Mock the WebOSAppContainer
jest.mock('../services/AppFramework');

describe('AppRegistry', () => {
  let appRegistry;
  let mockWindowManager;

  beforeEach(() => {
    appRegistry = new AppRegistry();
    mockWindowManager = {
      createWindow: jest.fn().mockResolvedValue('window-123')
    };
    
    // Clear all mocks
    jest.clearAllMocks();
    WebOSAppContainer.mockClear();
  });

  describe('App Registration', () => {
    test('should register an application successfully', () => {
      const appConfig = {
        id: 'test-app',
        name: 'Test Application',
        type: 'react',
        category: 'Testing',
        description: 'A test application'
      };

      appRegistry.registerApp(appConfig);

      expect(WebOSAppContainer).toHaveBeenCalledWith(appConfig);
      expect(appRegistry.registeredApps.has('test-app')).toBe(true);
    });

    test('should categorize applications correctly', () => {
      const appConfig1 = {
        id: 'app1',
        name: 'App 1',
        category: 'Development'
      };
      const appConfig2 = {
        id: 'app2',
        name: 'App 2',
        category: 'Development'
      };
      const appConfig3 = {
        id: 'app3',
        name: 'App 3',
        category: 'System'
      };

      appRegistry.registerApp(appConfig1);
      appRegistry.registerApp(appConfig2);
      appRegistry.registerApp(appConfig3);

      expect(appRegistry.appCategories.get('Development')).toEqual(['app1', 'app2']);
      expect(appRegistry.appCategories.get('System')).toEqual(['app3']);
    });

    test('should handle apps without category', () => {
      const appConfig = {
        id: 'no-category-app',
        name: 'No Category App'
      };

      appRegistry.registerApp(appConfig);

      expect(appRegistry.appCategories.get('General')).toEqual(['no-category-app']);
    });
  });

  describe('App Launching', () => {
    beforeEach(async () => {
      await appRegistry.initialize(mockWindowManager);
    });

    test('should launch an application successfully', async () => {
      const mockContainer = {
        initialized: true,
        initialize: jest.fn().mockResolvedValue(true),
        appName: 'Test App',
        component: 'TestComponent',
        getAppProps: jest.fn().mockReturnValue({}),
        appConfig: {
          icon: 'test-icon',
          defaultSize: { width: 800, height: 600 },
          minSize: { width: 400, height: 300 }
        }
      };

      appRegistry.registeredApps.set('test-app', mockContainer);

      const windowId = await appRegistry.launchApp('test-app');

      expect(mockWindowManager.createWindow).toHaveBeenCalledWith({
        title: 'Test App',
        component: 'TestComponent',
        props: {},
        icon: 'test-icon',
        defaultSize: { width: 800, height: 600 },
        minSize: { width: 400, height: 300 },
        resizable: true,
        maximizable: true,
        minimizable: true
      });
      expect(windowId).toBe('window-123');
      expect(appRegistry.runningApps.has('window-123')).toBe(true);
    });

    test('should initialize app container if not already initialized', async () => {
      const mockContainer = {
        initialized: false,
        initialize: jest.fn().mockResolvedValue(true),
        appName: 'Test App',
        component: 'TestComponent',
        getAppProps: jest.fn().mockReturnValue({}),
        appConfig: {}
      };

      appRegistry.registeredApps.set('test-app', mockContainer);

      await appRegistry.launchApp('test-app');

      expect(mockContainer.initialize).toHaveBeenCalled();
    });

    test('should throw error for non-existent app', async () => {
      await expect(appRegistry.launchApp('non-existent-app')).rejects.toThrow('App not found: non-existent-app');
    });

    test('should handle window manager not initialized', async () => {
      const appRegistryWithoutWM = new AppRegistry();
      const mockContainer = {
        initialized: true,
        appName: 'Test App'
      };
      appRegistryWithoutWM.registeredApps.set('test-app', mockContainer);

      await expect(appRegistryWithoutWM.launchApp('test-app')).rejects.toThrow('Window manager not initialized');
    });
  });

  describe('App Management', () => {
    beforeEach(() => {
      // Register some test apps
      appRegistry.registerApp({
        id: 'app1',
        name: 'Application 1',
        type: 'react',
        category: 'Development',
        description: 'First test app'
      });
      appRegistry.registerApp({
        id: 'app2',
        name: 'Application 2',
        type: 'iframe',
        category: 'System',
        description: 'Second test app'
      });
    });

    test('should get registered applications', () => {
      const apps = appRegistry.getRegisteredApps();

      expect(apps).toHaveLength(2);
      expect(apps[0]).toEqual({
        id: 'app1',
        name: 'Application 1',
        type: 'react',
        category: 'Development',
        icon: undefined,
        description: 'First test app'
      });
    });

    test('should get applications by category', () => {
      const devApps = appRegistry.getAppsByCategory('Development');
      const systemApps = appRegistry.getAppsByCategory('System');

      expect(devApps).toHaveLength(1);
      expect(systemApps).toHaveLength(1);
      expect(devApps[0].appId).toBe('app1');
      expect(systemApps[0].appId).toBe('app2');
    });

    test('should get all categories', () => {
      const categories = appRegistry.getCategories();

      expect(categories).toContain('Development');
      expect(categories).toContain('System');
    });

    test('should close running application', () => {
      const mockContainer = { appName: 'Test App' };
      appRegistry.runningApps.set('window-123', mockContainer);

      appRegistry.closeApp('window-123');

      expect(appRegistry.runningApps.has('window-123')).toBe(false);
    });

    test('should get running applications', () => {
      const mockContainer1 = { appId: 'app1', appName: 'App 1' };
      const mockContainer2 = { appId: 'app2', appName: 'App 2' };
      
      appRegistry.runningApps.set('window-1', mockContainer1);
      appRegistry.runningApps.set('window-2', mockContainer2);

      const runningApps = appRegistry.getRunningApps();

      expect(runningApps).toHaveLength(2);
      expect(runningApps[0]).toEqual({
        windowId: 'window-1',
        appId: 'app1',
        appName: 'App 1'
      });
    });
  });

  describe('Default Apps Registration', () => {
    test('should register all default JAEGIS applications', async () => {
      await appRegistry.registerDefaultApps();

      const registeredApps = appRegistry.getRegisteredApps();
      const appIds = registeredApps.map(app => app.id);

      // Check that all expected default apps are registered
      expect(appIds).toContain('jaegis-core');
      expect(appIds).toContain('nlds-terminal');
      expect(appIds).toContain('llm-os');
      expect(appIds).toContain('ai-chat');
      expect(appIds).toContain('ai-search');
      expect(appIds).toContain('deployment-center');
      expect(appIds).toContain('forge-console');
      expect(appIds).toContain('jaegis-cockpit');
      expect(appIds).toContain('text-editor');
      expect(appIds).toContain('file-explorer');
      expect(appIds).toContain('terminal');
      expect(appIds).toContain('system-info');
      expect(appIds).toContain('agent-coordination');
      expect(appIds).toContain('monitoring-dashboard');
    });

    test('should categorize default apps correctly', async () => {
      await appRegistry.registerDefaultApps();

      const categories = appRegistry.getCategories();
      
      expect(categories).toContain('Management');
      expect(categories).toContain('Research');
      expect(categories).toContain('AI');
      expect(categories).toContain('Development');
      expect(categories).toContain('System');

      const managementApps = appRegistry.getAppsByCategory('Management');
      const aiApps = appRegistry.getAppsByCategory('AI');
      
      expect(managementApps.length).toBeGreaterThan(0);
      expect(aiApps.length).toBeGreaterThan(0);
    });

    test('should set correct permissions for default apps', async () => {
      await appRegistry.registerDefaultApps();

      const cockpitApp = appRegistry.registeredApps.get('jaegis-cockpit');
      const terminalApp = appRegistry.registeredApps.get('terminal');

      expect(cockpitApp.permissions).toContain('system_access');
      expect(cockpitApp.permissions).toContain('agent_management');
      expect(terminalApp.permissions).toContain('system_access');
      expect(terminalApp.permissions).toContain('command_execution');
    });
  });

  describe('Initialization', () => {
    test('should initialize successfully with window manager', async () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      await appRegistry.initialize(mockWindowManager);

      expect(appRegistry.windowManager).toBe(mockWindowManager);
      expect(appRegistry.initialized).toBe(true);
      expect(consoleSpy).toHaveBeenCalledWith('✅ App Registry initialized');

      consoleSpy.mockRestore();
    });

    test('should register default apps during initialization', async () => {
      const registerDefaultAppsSpy = jest.spyOn(appRegistry, 'registerDefaultApps');

      await appRegistry.initialize(mockWindowManager);

      expect(registerDefaultAppsSpy).toHaveBeenCalled();
    });
  });
});
