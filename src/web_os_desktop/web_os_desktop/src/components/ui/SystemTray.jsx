// SystemTray.jsx - System Tray with Core Services Status
import React, { useState } from 'react';
import { useCoreServices } from '../../hooks/useCoreServices';

const SystemTray = () => {
  const { 
    serviceStatuses, 
    loading, 
    error, 
    performHealthCheck, 
    allServicesHealthy, 
    getHealthyServicesCount, 
    totalServices 
  } = useCoreServices();
  
  const [showDetails, setShowDetails] = useState(false);
  
  // Get status color
  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy': return 'bg-green-500';
      case 'unhealthy': return 'bg-red-500';
      case 'unknown': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };
  
  // Get overall system status
  const getOverallStatus = () => {
    if (loading) return { color: 'bg-blue-500', text: 'Loading...' };
    if (error) return { color: 'bg-red-500', text: 'Error' };
    if (allServicesHealthy()) return { color: 'bg-green-500', text: 'All Systems Operational' };
    
    const healthyCount = getHealthyServicesCount();
    return { 
      color: 'bg-yellow-500', 
      text: `${healthyCount}/${totalServices} Services Online` 
    };
  };
  
  const overallStatus = getOverallStatus();
  
  return (
    <div className="relative">
      {/* System Status Indicator */}
      <button
        onClick={() => setShowDetails(!showDetails)}
        className="flex items-center space-x-2 px-3 py-1 rounded-md hover:bg-gray-700 transition-colors"
        title="System Status"
      >
        <div className={`w-3 h-3 rounded-full ${overallStatus.color}`}></div>
        <span className="text-sm text-gray-300">System</span>
      </button>
      
      {/* Detailed Status Panel */}
      {showDetails && (
        <div className="absolute bottom-full right-0 mb-2 w-80 bg-gray-800 border border-gray-600 rounded-lg shadow-lg z-50">
          <div className="p-4">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">System Status</h3>
              <button
                onClick={performHealthCheck}
                disabled={loading}
                className="p-1 text-gray-400 hover:text-white transition-colors disabled:opacity-50"
                title="Refresh Status"
              >
                <svg className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </button>
            </div>
            
            {/* Overall Status */}
            <div className="flex items-center space-x-3 mb-4 p-3 bg-gray-700 rounded-lg">
              <div className={`w-4 h-4 rounded-full ${overallStatus.color}`}></div>
              <span className="text-white font-medium">{overallStatus.text}</span>
            </div>
            
            {/* Error Display */}
            {error && (
              <div className="mb-4 p-3 bg-red-900 border border-red-700 rounded-lg">
                <p className="text-red-300 text-sm">{error}</p>
              </div>
            )}
            
            {/* Service List */}
            <div className="space-y-2">
              <h4 className="text-sm font-medium text-gray-400 mb-2">Core Services</h4>
              {serviceStatuses.map((service) => (
                <div key={service.service} className="flex items-center justify-between p-2 bg-gray-700 rounded">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${getStatusColor(service.status)}`}></div>
                    <span className="text-white text-sm font-medium">{service.service}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-gray-400 capitalize">{service.status}</div>
                    {service.lastCheck && (
                      <div className="text-xs text-gray-500">
                        {new Date(service.lastCheck).toLocaleTimeString()}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
            
            {/* Service Details */}
            <div className="mt-4 pt-4 border-t border-gray-600">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-400">Total Services:</span>
                  <span className="text-white ml-2">{totalServices}</span>
                </div>
                <div>
                  <span className="text-gray-400">Online:</span>
                  <span className="text-green-400 ml-2">{getHealthyServicesCount()}</span>
                </div>
              </div>
            </div>
            
            {/* Quick Actions */}
            <div className="mt-4 pt-4 border-t border-gray-600">
              <div className="flex space-x-2">
                <button
                  onClick={() => window.open('http://localhost:8090', '_blank')}
                  className="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors"
                >
                  Open Cockpit
                </button>
                <button
                  onClick={() => setShowDetails(false)}
                  className="px-3 py-2 bg-gray-600 hover:bg-gray-500 text-white text-sm rounded transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Service Status Badge Component
export const ServiceStatusBadge = ({ serviceName, showLabel = true }) => {
  const { getServiceStatus } = useCoreServices();
  const status = getServiceStatus(serviceName);
  
  const getStatusColor = (status) => {
    switch (status?.status) {
      case 'healthy': return 'bg-green-500';
      case 'unhealthy': return 'bg-red-500';
      case 'unknown': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };
  
  return (
    <div className="flex items-center space-x-2">
      <div className={`w-2 h-2 rounded-full ${getStatusColor(status)}`}></div>
      {showLabel && (
        <span className="text-xs text-gray-400">{serviceName}</span>
      )}
    </div>
  );
};

export default SystemTray;
