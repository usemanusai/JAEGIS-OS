/**
 * JAEGIS Cockpit Configuration
 * 
 * Centralized configuration for API endpoints and system settings.
 * This replaces all hardcoded localhost URLs with configurable values.
 */

// Environment-based configuration
const isDevelopment = import.meta.env.DEV;
const isProduction = import.meta.env.PROD;

// API Configuration
export const API_CONFIG = {
  // Backend API Base URL
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8090',
  
  // WebSocket Configuration
  WS_BASE_URL: import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8090',
  
  // API Endpoints
  ENDPOINTS: {
    // System endpoints
    SYSTEM_STATUS: '/api/system/status',
    HEALTH: '/health',
    
    // A.C.I.D. Swarm endpoints
    ACID_SWARMS: '/api/acid/swarms',
    ACID_TASKS: '/api/acid/tasks',
    ACID_SWARM_DETAIL: (id) => `/api/acid/swarms/${id}`,
    
    // Agent System endpoints
    AGENTS: '/api/agents',
    AGENTS_ACTIVE: '/api/agents/active',
    AGENTS_TIERS: '/api/agents/tiers',
    AGENT_DETAIL: (id) => `/api/agents/${id}`,
    
    // N.L.D.S. endpoints
    NLDS_STATS: '/api/nlds/stats',
    NLDS_LANGUAGES: '/api/nlds/languages',
    NLDS_DETECT: '/api/nlds/detect',
    
    // Enhanced Chat System endpoints
    CHAT_SESSIONS: '/api/chat/sessions',
    CHAT_MODELS: '/api/chat/models',
    CHAT_METRICS: '/api/chat/metrics',
    
    // WebSocket endpoints
    WS_SYSTEM_STATUS: '/ws/system-status'
  },
  
  // Request configuration
  TIMEOUT: parseInt(import.meta.env.VITE_API_TIMEOUT) || 10000, // 10 seconds
  RETRY_ATTEMPTS: parseInt(import.meta.env.VITE_API_RETRY_ATTEMPTS) || 3,
  RETRY_DELAY: parseInt(import.meta.env.VITE_API_RETRY_DELAY) || 1000, // 1 second
};

// WebSocket Configuration
export const WS_CONFIG = {
  RECONNECT_INTERVAL: 5000, // 5 seconds
  MAX_RECONNECT_ATTEMPTS: 10,
  HEARTBEAT_INTERVAL: 30000, // 30 seconds
};

// Application Configuration
export const APP_CONFIG = {
  NAME: 'JAEGIS Cockpit',
  VERSION: '2.0.0',
  DESCRIPTION: 'Real-Time Operational Dashboard for the JAEGIS Ecosystem',
  
  // Feature flags
  FEATURES: {
    REAL_TIME_MONITORING: true,
    ACID_SWARM_MONITORING: true,
    AGENT_SYSTEM_MONITORING: true,
    NLDS_INTEGRATION: true,
    CHAT_SYSTEM_MONITORING: true,
    ERROR_REPORTING: isDevelopment,
    DEBUG_MODE: isDevelopment,
  },
  
  // UI Configuration
  UI: {
    REFRESH_INTERVAL: 2000, // 2 seconds for real-time updates
    CHART_UPDATE_INTERVAL: 5000, // 5 seconds for charts
    NOTIFICATION_TIMEOUT: 5000, // 5 seconds
    MAX_LOG_ENTRIES: 100,
  },
  
  // Development settings
  DEV: {
    MOCK_DATA: false, // No mock data - all real integrations
    VERBOSE_LOGGING: isDevelopment,
    SHOW_DEBUG_INFO: isDevelopment,
  }
};

// Utility functions for API calls
export const API_UTILS = {
  /**
   * Get full API URL
   */
  getApiUrl: (endpoint) => {
    return `${API_CONFIG.BASE_URL}${endpoint}`;
  },
  
  /**
   * Get full WebSocket URL
   */
  getWsUrl: (endpoint) => {
    return `${API_CONFIG.WS_BASE_URL}${endpoint}`;
  },
  
  /**
   * Default fetch options with timeout and error handling
   */
  getDefaultFetchOptions: () => ({
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    signal: AbortSignal.timeout(API_CONFIG.TIMEOUT),
  }),
  
  /**
   * Enhanced fetch with retry logic
   */
  fetchWithRetry: async (url, options = {}, retries = API_CONFIG.RETRY_ATTEMPTS) => {
    try {
      const response = await fetch(url, {
        ...API_UTILS.getDefaultFetchOptions(),
        ...options,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response;
    } catch (error) {
      if (retries > 0 && !error.name === 'AbortError') {
        console.warn(`API call failed, retrying... (${retries} attempts left)`);
        await new Promise(resolve => setTimeout(resolve, API_CONFIG.RETRY_DELAY));
        return API_UTILS.fetchWithRetry(url, options, retries - 1);
      }
      throw error;
    }
  }
};

// Export configuration for environment detection
export const ENV = {
  isDevelopment,
  isProduction,
  NODE_ENV: import.meta.env.MODE,
};

// Validation
if (isDevelopment) {
  console.log('🔧 JAEGIS Cockpit Configuration:', {
    API_BASE_URL: API_CONFIG.BASE_URL,
    WS_BASE_URL: API_CONFIG.WS_BASE_URL,
    FEATURES: APP_CONFIG.FEATURES,
    ENV: ENV.NODE_ENV,
  });
}
