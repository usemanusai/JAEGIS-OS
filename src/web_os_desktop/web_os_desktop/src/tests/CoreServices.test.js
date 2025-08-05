// CoreServices.test.js - Tests for Core Service Integration
import { 
  CoreServiceManager, 
  SCRIPTClient, 
  ATLASClient, 
  HELMClient, 
  MASTRClient, 
  ASCENDClient, 
  CORIClient, 
  NLDSClient 
} from '../services/CoreServiceClients';

// Mock fetch globally
global.fetch = jest.fn();

describe('Core Service Clients', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  describe('BaseAPIClient', () => {
    let scriptClient;

    beforeEach(() => {
      scriptClient = new SCRIPTClient();
    });

    test('should make authenticated API request successfully', async () => {
      const mockResponse = { data: 'test' };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await scriptClient.request('/test');

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8080/test',
        expect.objectContaining({
          headers: expect.objectContaining({
            'Content-Type': 'application/json'
          })
        })
      );
      expect(result).toEqual(mockResponse);
    });

    test('should handle API request errors', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error'
      });

      await expect(scriptClient.request('/test')).rejects.toThrow('S.C.R.I.P.T. API error: 500 Internal Server Error');
    });

    test('should handle network errors', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'));

      await expect(scriptClient.request('/test')).rejects.toThrow('Network error');
    });

    test('should perform health check', async () => {
      const mockHealthResponse = { status: 'healthy', timestamp: '2023-01-01T00:00:00Z' };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockHealthResponse
      });

      const result = await scriptClient.healthCheck();

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8080/health',
        expect.any(Object)
      );
      expect(result).toEqual(mockHealthResponse);
      expect(scriptClient.healthStatus).toBe('healthy');
      expect(scriptClient.lastHealthCheck).toBeTruthy();
    });

    test('should handle health check failure', async () => {
      fetch.mockRejectedValueOnce(new Error('Service unavailable'));

      await expect(scriptClient.healthCheck()).rejects.toThrow('Service unavailable');
      expect(scriptClient.healthStatus).toBe('unhealthy');
    });

    test('should get service status', () => {
      scriptClient.healthStatus = 'healthy';
      scriptClient.lastHealthCheck = '2023-01-01T00:00:00Z';

      const status = scriptClient.getStatus();

      expect(status).toEqual({
        service: 'S.C.R.I.P.T.',
        status: 'healthy',
        lastCheck: '2023-01-01T00:00:00Z',
        url: 'http://localhost:8080'
      });
    });
  });

  describe('S.C.R.I.P.T. Client', () => {
    let scriptClient;

    beforeEach(() => {
      scriptClient = new SCRIPTClient();
    });

    test('should get Web OS configuration', async () => {
      const mockConfig = { theme: 'dark', layout: 'desktop' };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConfig
      });

      const result = await scriptClient.getWebOSConfig();

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8080/api/config/webos',
        expect.any(Object)
      );
      expect(result).toEqual(mockConfig);
    });

    test('should update Web OS settings', async () => {
      const settings = { theme: 'light' };
      const mockResponse = { success: true };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await scriptClient.updateWebOSSettings(settings);

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8080/api/config/webos',
        expect.objectContaining({
          method: 'PUT',
          body: JSON.stringify(settings)
        })
      );
      expect(result).toEqual(mockResponse);
    });

    test('should get user preferences', async () => {
      const mockPreferences = { notifications: true, autoSave: false };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockPreferences
      });

      const result = await scriptClient.getUserPreferences('user123');

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8080/api/config/users/user123/preferences',
        expect.any(Object)
      );
      expect(result).toEqual(mockPreferences);
    });
  });

  describe('A.T.L.A.S. Client', () => {
    let atlasClient;

    beforeEach(() => {
      atlasClient = new ATLASClient();
    });

    test('should sync application data', async () => {
      const mockResponse = { synced: true, timestamp: '2023-01-01T00:00:00Z' };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await atlasClient.syncAppData('app123');

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8081/api/sync/apps/app123',
        expect.objectContaining({ method: 'POST' })
      );
      expect(result).toEqual(mockResponse);
    });

    test('should get GitHub workspace', async () => {
      const mockWorkspace = { repositories: [], branches: [] };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockWorkspace
      });

      const result = await atlasClient.getGitHubWorkspace();

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8081/api/github/workspace',
        expect.any(Object)
      );
      expect(result).toEqual(mockWorkspace);
    });
  });

  describe('H.E.L.M. Client', () => {
    let helmClient;

    beforeEach(() => {
      helmClient = new HELMClient();
    });

    test('should get real-time metrics', async () => {
      const mockMetrics = { cpu: 45, memory: 60, network: 25 };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockMetrics
      });

      const result = await helmClient.getRealTimeMetrics();

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8082/api/metrics/realtime',
        expect.any(Object)
      );
      expect(result).toEqual(mockMetrics);
    });

    test('should run performance benchmark', async () => {
      const testSuite = { tests: ['cpu', 'memory', 'disk'] };
      const mockResults = { passed: 3, failed: 0, duration: 120 };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResults
      });

      const result = await helmClient.runPerformanceBenchmark(testSuite);

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8082/api/benchmark/run',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(testSuite)
        })
      );
      expect(result).toEqual(mockResults);
    });
  });

  describe('N.L.D.S. Client', () => {
    let nldsClient;

    beforeEach(() => {
      nldsClient = new NLDSClient();
    });

    test('should process natural language command', async () => {
      const command = 'open file explorer';
      const mockResponse = { 
        intent: 'open_application', 
        confidence: 0.95, 
        parameters: { appName: 'file-explorer' } 
      };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await nldsClient.processCommand(command);

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/nlp/process',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ command })
        })
      );
      expect(result).toEqual(mockResponse);
    });

    test('should get command suggestions', async () => {
      const partial = 'open';
      const mockSuggestions = { suggestions: ['open file', 'open terminal', 'open settings'] };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockSuggestions
      });

      const result = await nldsClient.getCommandSuggestions(partial);

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/nlp/suggestions?q=open',
        expect.any(Object)
      );
      expect(result).toEqual(mockSuggestions);
    });
  });
});

describe('CoreServiceManager', () => {
  let serviceManager;

  beforeEach(() => {
    serviceManager = new CoreServiceManager();
    fetch.mockClear();
  });

  afterEach(() => {
    serviceManager.stopHealthMonitoring();
  });

  test('should initialize all services', async () => {
    // Mock successful health checks for all services
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'healthy' })
    });

    await serviceManager.initialize();

    expect(serviceManager.healthCheckInterval).toBeTruthy();
    expect(fetch).toHaveBeenCalledTimes(7); // 7 core services
  });

  test('should get service by name', () => {
    const scriptService = serviceManager.getService('script');
    const atlasService = serviceManager.getService('ATLAS');

    expect(scriptService).toBeInstanceOf(SCRIPTClient);
    expect(atlasService).toBeInstanceOf(ATLASClient);
  });

  test('should get all service statuses', () => {
    // Set some mock statuses
    serviceManager.services.script.healthStatus = 'healthy';
    serviceManager.services.atlas.healthStatus = 'unhealthy';

    const statuses = serviceManager.getAllStatuses();

    expect(statuses).toHaveLength(7);
    expect(statuses.find(s => s.service === 'S.C.R.I.P.T.').status).toBe('healthy');
    expect(statuses.find(s => s.service === 'A.T.L.A.S.').status).toBe('unhealthy');
  });

  test('should perform health checks on all services', async () => {
    // Mock mixed health check results
    fetch
      .mockResolvedValueOnce({ ok: true, json: async () => ({ status: 'healthy' }) })
      .mockRejectedValueOnce(new Error('Service unavailable'))
      .mockResolvedValueOnce({ ok: true, json: async () => ({ status: 'healthy' }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ status: 'healthy' }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ status: 'healthy' }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ status: 'healthy' }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ status: 'healthy' }) });

    const results = await serviceManager.performHealthChecks();

    expect(results).toHaveLength(7);
    expect(fetch).toHaveBeenCalledTimes(7);
  });

  test('should start and stop health monitoring', () => {
    serviceManager.startHealthMonitoring(1000); // 1 second interval
    expect(serviceManager.healthCheckInterval).toBeTruthy();

    serviceManager.stopHealthMonitoring();
    expect(serviceManager.healthCheckInterval).toBe(null);
  });

  test('should handle status update subscriptions', () => {
    const mockCallback = jest.fn();
    const unsubscribe = serviceManager.onStatusUpdate(mockCallback);

    serviceManager.notifyStatusCallbacks();

    expect(mockCallback).toHaveBeenCalledWith(expect.any(Array));

    unsubscribe();
    serviceManager.notifyStatusCallbacks();

    expect(mockCallback).toHaveBeenCalledTimes(1); // Should not be called again after unsubscribe
  });
});
