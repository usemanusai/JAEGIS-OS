// JAEGIS Cockpit App - Iframe Integration
import React, { useRef, useEffect, useState } from 'react';
import { useAuth } from '../../hooks/useAuth';

const CockpitApp = ({ appId, appName, communication, state, permissions }) => {
  const iframeRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('connecting');
  const { getAuthHeader } = useAuth();
  
  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    
    const handleLoad = () => {
      setLoading(false);
      setConnectionStatus('connected');
      initializeCommunication();
    };
    
    const handleError = () => {
      setError('Failed to load Cockpit interface');
      setLoading(false);
      setConnectionStatus('error');
    };
    
    iframe.addEventListener('load', handleLoad);
    iframe.addEventListener('error', handleError);
    
    // Set up cross-frame communication
    setupMessageHandling();
    
    return () => {
      iframe.removeEventListener('load', handleLoad);
      iframe.removeEventListener('error', handleError);
    };
  }, []);
  
  // Initialize communication with Cockpit
  const initializeCommunication = () => {
    const iframe = iframeRef.current;
    if (!iframe || !iframe.contentWindow) return;
    
    // Send authentication token to Cockpit
    sendToCockpit('auth_token', {
      token: getAuthHeader(),
      user: state.get('currentUser'),
      permissions: permissions
    });
    
    // Send initial configuration
    sendToCockpit('webos_config', {
      appId: appId,
      appName: appName,
      theme: state.get('theme') || 'dark'
    });
  };
  
  // Set up message handling from Cockpit
  const setupMessageHandling = () => {
    const handleMessage = (event) => {
      // Verify origin for security
      if (event.origin !== 'http://localhost:8090') return;
      
      const { type, data } = event.data;
      
      switch (type) {
        case 'system_status_update':
          handleSystemStatusUpdate(data);
          break;
        case 'agent_status_update':
          handleAgentStatusUpdate(data);
          break;
        case 'navigation_request':
          handleNavigationRequest(data);
          break;
        case 'cockpit_ready':
          handleCockpitReady(data);
          break;
        case 'error':
          handleCockpitError(data);
          break;
        default:
          console.log('Unknown Cockpit message:', type, data);
      }
    };
    
    window.addEventListener('message', handleMessage);
    
    return () => window.removeEventListener('message', handleMessage);
  };
  
  // Send message to Cockpit
  const sendToCockpit = (type, data) => {
    const iframe = iframeRef.current;
    if (iframe && iframe.contentWindow) {
      iframe.contentWindow.postMessage({
        type,
        data,
        source: 'webos',
        timestamp: new Date().toISOString()
      }, 'http://localhost:8090');
    }
  };
  
  // Handle system status updates from Cockpit
  const handleSystemStatusUpdate = (data) => {
    // Update Web OS system tray
    communication.sendMessage('system-tray', 'status_update', data);
    
    // Update local state
    state.set('systemStatus', data);
    
    // Emit global event
    const event = new CustomEvent('system-status-update', { detail: data });
    window.dispatchEvent(event);
  };
  
  // Handle agent status updates from Cockpit
  const handleAgentStatusUpdate = (data) => {
    // Update Web OS agent indicators
    communication.sendMessage('agent-monitor', 'agent_update', data);
    
    // Update local state
    state.set('agentStatus', data);
    
    // Emit global event
    const event = new CustomEvent('agent-status-update', { detail: data });
    window.dispatchEvent(event);
  };
  
  // Handle navigation requests from Cockpit
  const handleNavigationRequest = (data) => {
    const { action, target, params } = data;
    
    switch (action) {
      case 'open_app':
        communication.sendMessage('app-launcher', 'launch_app', { appId: target, params });
        break;
      case 'focus_window':
        communication.sendMessage('window-manager', 'focus_window', { windowId: target });
        break;
      case 'show_notification':
        communication.sendMessage('notification-system', 'show_notification', params);
        break;
      default:
        console.log('Unknown navigation request:', action, target);
    }
  };
  
  // Handle Cockpit ready signal
  const handleCockpitReady = (data) => {
    setConnectionStatus('ready');
    console.log('✅ Cockpit is ready:', data);
    
    // Send any queued messages or initial data
    sendToCockpit('webos_ready', {
      timestamp: new Date().toISOString(),
      version: '1.0.0'
    });
  };
  
  // Handle Cockpit errors
  const handleCockpitError = (data) => {
    console.error('❌ Cockpit error:', data);
    setError(data.message || 'Cockpit error occurred');
    setConnectionStatus('error');
  };
  
  // Refresh Cockpit iframe
  const refreshCockpit = () => {
    setLoading(true);
    setError(null);
    setConnectionStatus('connecting');
    
    const iframe = iframeRef.current;
    if (iframe) {
      iframe.src = iframe.src; // Reload iframe
    }
  };
  
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-full bg-gray-900 text-white">
        <div className="text-center">
          <svg className="mx-auto h-12 w-12 text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <h3 className="text-lg font-medium mb-2">Connection Error</h3>
          <p className="text-gray-400 mb-4">{error}</p>
          <button
            onClick={refreshCockpit}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-md transition-colors"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }
  
  return (
    <div className="relative w-full h-full bg-gray-900">
      {/* Connection Status Bar */}
      <div className="absolute top-0 left-0 right-0 z-10 bg-gray-800 border-b border-gray-700 px-4 py-2 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${
            connectionStatus === 'connected' || connectionStatus === 'ready' ? 'bg-green-500' :
            connectionStatus === 'connecting' ? 'bg-yellow-500' :
            'bg-red-500'
          }`}></div>
          <span className="text-sm text-gray-300">
            {connectionStatus === 'connected' ? 'Connected' :
             connectionStatus === 'ready' ? 'Ready' :
             connectionStatus === 'connecting' ? 'Connecting...' :
             'Disconnected'}
          </span>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={refreshCockpit}
            className="p-1 text-gray-400 hover:text-white transition-colors"
            title="Refresh Cockpit"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
      </div>
      
      {/* Loading Overlay */}
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-900 z-20">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading JAEGIS Cockpit...</p>
          </div>
        </div>
      )}
      
      {/* Cockpit Iframe */}
      <iframe
        ref={iframeRef}
        src="http://localhost:8090"
        className="w-full h-full border-0"
        style={{ marginTop: '40px', height: 'calc(100% - 40px)' }}
        title="JAEGIS Cockpit"
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
        allow="fullscreen"
      />
    </div>
  );
};

export default CockpitApp;
