// RealTimeMonitoringDashboard.jsx - Real-time System Monitoring
import React, { useState, useEffect } from 'react';
import { useHELM, useCoreServices } from '../../hooks/useCoreServices';

const RealTimeMonitoringDashboard = () => {
  const [systemMetrics, setSystemMetrics] = useState({
    cpu: { usage: 0, cores: 8, temperature: 0 },
    memory: { used: 0, total: 16384, available: 0 },
    network: { upload: 0, download: 0, latency: 0 },
    disk: { used: 0, total: 1024, read: 0, write: 0 }
  });
  
  const [performanceHistory, setPerformanceHistory] = useState({
    cpu: [],
    memory: [],
    network: []
  });
  
  const [alerts, setAlerts] = useState([]);
  const [appPerformance, setAppPerformance] = useState([]);
  
  const { service: helmService, isHealthy: helmHealthy } = useHELM();
  const { serviceStatuses, allServicesHealthy } = useCoreServices();
  
  useEffect(() => {
    updateMetrics();
    const interval = setInterval(updateMetrics, 2000); // Update every 2 seconds
    return () => clearInterval(interval);
  }, []);
  
  // Update system metrics
  const updateMetrics = async () => {
    try {
      if (helmHealthy && helmService) {
        const realTimeMetrics = await helmService.getRealTimeMetrics();
        setSystemMetrics(realTimeMetrics);
        
        const qualityMetrics = await helmService.getQualityMetrics();
        setAppPerformance(qualityMetrics.applications || []);
      } else {
        // Simulate metrics for demo
        simulateMetrics();
      }
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
      simulateMetrics();
    }
  };
  
  // Simulate metrics for demo
  const simulateMetrics = () => {
    const now = Date.now();
    
    setSystemMetrics(prev => {
      const newMetrics = {
        cpu: {
          usage: Math.max(10, Math.min(90, prev.cpu.usage + (Math.random() - 0.5) * 10)),
          cores: 8,
          temperature: Math.max(40, Math.min(80, prev.cpu.temperature + (Math.random() - 0.5) * 5))
        },
        memory: {
          used: Math.max(2048, Math.min(14336, prev.memory.used + (Math.random() - 0.5) * 512)),
          total: 16384,
          available: 16384 - prev.memory.used
        },
        network: {
          upload: Math.max(0, Math.min(100, prev.network.upload + (Math.random() - 0.5) * 20)),
          download: Math.max(0, Math.min(100, prev.network.download + (Math.random() - 0.5) * 20)),
          latency: Math.max(10, Math.min(200, prev.network.latency + (Math.random() - 0.5) * 20))
        },
        disk: {
          used: Math.max(100, Math.min(900, prev.disk.used + (Math.random() - 0.5) * 10)),
          total: 1024,
          read: Math.max(0, Math.min(50, prev.disk.read + (Math.random() - 0.5) * 10)),
          write: Math.max(0, Math.min(50, prev.disk.write + (Math.random() - 0.5) * 10))
        }
      };
      
      // Update performance history
      setPerformanceHistory(prevHistory => ({
        cpu: [...prevHistory.cpu.slice(-29), { time: now, value: newMetrics.cpu.usage }],
        memory: [...prevHistory.memory.slice(-29), { time: now, value: (newMetrics.memory.used / newMetrics.memory.total) * 100 }],
        network: [...prevHistory.network.slice(-29), { time: now, value: newMetrics.network.download }]
      }));
      
      return newMetrics;
    });
    
    // Check for alerts
    checkAlerts();
  };
  
  // Check for performance alerts
  const checkAlerts = () => {
    const newAlerts = [];
    
    if (systemMetrics.cpu.usage > 80) {
      newAlerts.push({
        id: 'cpu-high',
        type: 'warning',
        message: `High CPU usage: ${Math.round(systemMetrics.cpu.usage)}%`,
        timestamp: new Date().toISOString()
      });
    }
    
    if ((systemMetrics.memory.used / systemMetrics.memory.total) > 0.85) {
      newAlerts.push({
        id: 'memory-high',
        type: 'warning',
        message: `High memory usage: ${Math.round((systemMetrics.memory.used / systemMetrics.memory.total) * 100)}%`,
        timestamp: new Date().toISOString()
      });
    }
    
    if (!allServicesHealthy()) {
      newAlerts.push({
        id: 'service-down',
        type: 'error',
        message: 'One or more core services are unhealthy',
        timestamp: new Date().toISOString()
      });
    }
    
    setAlerts(newAlerts);
  };
  
  // Format bytes
  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };
  
  // Get status color
  const getStatusColor = (value, thresholds = { warning: 70, critical: 90 }) => {
    if (value >= thresholds.critical) return 'text-red-400';
    if (value >= thresholds.warning) return 'text-yellow-400';
    return 'text-green-400';
  };
  
  // Get progress bar color
  const getProgressColor = (value, thresholds = { warning: 70, critical: 90 }) => {
    if (value >= thresholds.critical) return 'bg-red-500';
    if (value >= thresholds.warning) return 'bg-yellow-500';
    return 'bg-green-500';
  };
  
  // Simple line chart component
  const MiniChart = ({ data, color = 'rgb(59, 130, 246)' }) => {
    if (data.length < 2) return <div className="h-16 bg-gray-700 rounded"></div>;
    
    const maxValue = Math.max(...data.map(d => d.value));
    const minValue = Math.min(...data.map(d => d.value));
    const range = maxValue - minValue || 1;
    
    const points = data.map((point, index) => {
      const x = (index / (data.length - 1)) * 100;
      const y = 100 - ((point.value - minValue) / range) * 100;
      return `${x},${y}`;
    }).join(' ');
    
    return (
      <div className="h-16 bg-gray-700 rounded p-2">
        <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
          <polyline
            fill="none"
            stroke={color}
            strokeWidth="2"
            points={points}
          />
        </svg>
      </div>
    );
  };
  
  return (
    <div className="p-6 bg-gray-900 text-white min-h-screen">
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-2">Real-time Monitoring Dashboard</h1>
        <p className="text-gray-400">Live system performance and health monitoring</p>
      </div>
      
      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="mb-6">
          <h2 className="text-lg font-semibold mb-3">Active Alerts</h2>
          <div className="space-y-2">
            {alerts.map((alert) => (
              <div key={alert.id} className={`p-3 rounded-lg border-l-4 ${
                alert.type === 'error' ? 'bg-red-900 border-red-500' : 'bg-yellow-900 border-yellow-500'
              }`}>
                <div className="flex items-center justify-between">
                  <span>{alert.message}</span>
                  <span className="text-xs text-gray-400">
                    {new Date(alert.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* System Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        {/* CPU Usage */}
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">CPU Usage</h3>
            <span className={`text-2xl font-bold ${getStatusColor(systemMetrics.cpu.usage)}`}>
              {Math.round(systemMetrics.cpu.usage)}%
            </span>
          </div>
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-1">
              <span>Usage</span>
              <span>{Math.round(systemMetrics.cpu.usage)}%</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${getProgressColor(systemMetrics.cpu.usage)}`}
                style={{ width: `${systemMetrics.cpu.usage}%` }}
              ></div>
            </div>
          </div>
          <MiniChart data={performanceHistory.cpu} color="rgb(59, 130, 246)" />
          <div className="mt-2 text-xs text-gray-400">
            Cores: {systemMetrics.cpu.cores} | Temp: {Math.round(systemMetrics.cpu.temperature)}°C
          </div>
        </div>
        
        {/* Memory Usage */}
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Memory</h3>
            <span className={`text-2xl font-bold ${getStatusColor((systemMetrics.memory.used / systemMetrics.memory.total) * 100)}`}>
              {Math.round((systemMetrics.memory.used / systemMetrics.memory.total) * 100)}%
            </span>
          </div>
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-1">
              <span>Used</span>
              <span>{formatBytes(systemMetrics.memory.used * 1024 * 1024)}</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${getProgressColor((systemMetrics.memory.used / systemMetrics.memory.total) * 100)}`}
                style={{ width: `${(systemMetrics.memory.used / systemMetrics.memory.total) * 100}%` }}
              ></div>
            </div>
          </div>
          <MiniChart data={performanceHistory.memory} color="rgb(34, 197, 94)" />
          <div className="mt-2 text-xs text-gray-400">
            Total: {formatBytes(systemMetrics.memory.total * 1024 * 1024)}
          </div>
        </div>
        
        {/* Network Activity */}
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Network</h3>
            <span className="text-2xl font-bold text-blue-400">
              {Math.round(systemMetrics.network.download)} Mbps
            </span>
          </div>
          <div className="mb-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span>Download</span>
              <span>{Math.round(systemMetrics.network.download)} Mbps</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Upload</span>
              <span>{Math.round(systemMetrics.network.upload)} Mbps</span>
            </div>
          </div>
          <MiniChart data={performanceHistory.network} color="rgb(168, 85, 247)" />
          <div className="mt-2 text-xs text-gray-400">
            Latency: {Math.round(systemMetrics.network.latency)}ms
          </div>
        </div>
        
        {/* Disk Usage */}
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Disk</h3>
            <span className={`text-2xl font-bold ${getStatusColor((systemMetrics.disk.used / systemMetrics.disk.total) * 100)}`}>
              {Math.round((systemMetrics.disk.used / systemMetrics.disk.total) * 100)}%
            </span>
          </div>
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-1">
              <span>Used</span>
              <span>{formatBytes(systemMetrics.disk.used * 1024 * 1024 * 1024)}</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${getProgressColor((systemMetrics.disk.used / systemMetrics.disk.total) * 100)}`}
                style={{ width: `${(systemMetrics.disk.used / systemMetrics.disk.total) * 100}%` }}
              ></div>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2 text-xs text-gray-400">
            <div>Read: {Math.round(systemMetrics.disk.read)} MB/s</div>
            <div>Write: {Math.round(systemMetrics.disk.write)} MB/s</div>
          </div>
        </div>
      </div>
      
      {/* Core Services Status */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Core Services Health</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {serviceStatuses.map((service) => (
            <div key={service.service} className="bg-gray-700 rounded p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">{service.service}</span>
                <div className={`w-3 h-3 rounded-full ${
                  service.status === 'healthy' ? 'bg-green-500' : 
                  service.status === 'unhealthy' ? 'bg-red-500' : 'bg-yellow-500'
                }`}></div>
              </div>
              <div className="text-sm text-gray-400 capitalize">{service.status}</div>
              {service.lastCheck && (
                <div className="text-xs text-gray-500 mt-1">
                  Last check: {new Date(service.lastCheck).toLocaleTimeString()}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RealTimeMonitoringDashboard;
