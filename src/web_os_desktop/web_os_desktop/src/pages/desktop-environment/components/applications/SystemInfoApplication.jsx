import React, { useState, useEffect } from 'react';
import Icon from '../../../../components/AppIcon';

const SystemInfoApplication = ({ windowId }) => {
  const [systemInfo, setSystemInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call to fetch system information
    const fetchSystemInfo = async () => {
      setLoading(true);
      
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock system information
      const mockSystemInfo = {
        system: {
          name: 'Web OS',
          version: '1.0.0',
          build: '2024.07.31',
          architecture: 'x64',
          platform: navigator.platform,
          userAgent: navigator.userAgent?.substring(0, 80) + '...'
        },
        hardware: {
          processor: 'Intel Core i7-12700K @ 3.60GHz',
          cores: navigator.hardwareConcurrency || 8,
          memory: '16 GB DDR4',
          graphics: 'NVIDIA GeForce RTX 3070',
          storage: '1 TB NVMe SSD'
        },
        browser: {
          name: getBrowserName(),
          version: getBrowserVersion(),
          language: navigator.language,
          cookieEnabled: navigator.cookieEnabled,
          onlineStatus: navigator.onLine ? 'Online' : 'Offline'
        },
        display: {
          resolution: `${screen.width} x ${screen.height}`,
          colorDepth: `${screen.colorDepth}-bit`,
          pixelRatio: window.devicePixelRatio,
          orientation: screen.orientation?.type || 'landscape-primary'
        },
        network: {
          connection: getConnectionInfo(),
          effectiveType: navigator.connection?.effectiveType || 'Unknown',
          downlink: navigator.connection?.downlink ? `${navigator.connection?.downlink} Mbps` : 'Unknown',
          rtt: navigator.connection?.rtt ? `${navigator.connection?.rtt} ms` : 'Unknown'
        },
        performance: {
          uptime: formatUptime(performance.now()),
          memoryUsage: getMemoryUsage(),
          timing: getPerformanceTiming()
        }
      };
      
      setSystemInfo(mockSystemInfo);
      setLoading(false);
    };

    fetchSystemInfo();
  }, []);

  const getBrowserName = () => {
    const userAgent = navigator.userAgent;
    if (userAgent?.includes('Chrome')) return 'Google Chrome';
    if (userAgent?.includes('Firefox')) return 'Mozilla Firefox';
    if (userAgent?.includes('Safari')) return 'Safari';
    if (userAgent?.includes('Edge')) return 'Microsoft Edge';
    return 'Unknown Browser';
  };

  const getBrowserVersion = () => {
    const userAgent = navigator.userAgent;
    const match = userAgent?.match(/(Chrome|Firefox|Safari|Edge)\/(\d+)/);
    return match ? match?.[2] : 'Unknown';
  };

  const getConnectionInfo = () => {
    if (!navigator.connection) return 'Unknown';
    return navigator.connection?.type || 'Unknown';
  };

  const formatUptime = (milliseconds) => {
    const seconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
  };

  const getMemoryUsage = () => {
    if (performance.memory) {
      const used = Math.round(performance.memory?.usedJSHeapSize / 1024 / 1024);
      const total = Math.round(performance.memory?.totalJSHeapSize / 1024 / 1024);
      return `${used} MB / ${total} MB`;
    }
    return 'Not available';
  };

  const getPerformanceTiming = () => {
    const timing = performance.timing;
    const loadTime = timing?.loadEventEnd - timing?.navigationStart;
    return `${loadTime} ms`;
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center bg-background">
        <div className="text-center">
          <Icon name="Loader2" size={32} className="animate-spin text-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Loading system information...</p>
        </div>
      </div>
    );
  }

  const InfoSection = ({ title, icon, data }) => (
    <div className="bg-surface rounded-lg p-4 border border-border">
      <div className="flex items-center space-x-2 mb-3">
        <Icon name={icon} size={20} className="text-primary" />
        <h3 className="font-semibold text-foreground">{title}</h3>
      </div>
      <div className="space-y-2">
        {Object.entries(data)?.map(([key, value]) => (
          <div key={key} className="flex justify-between items-center">
            <span className="text-sm text-muted-foreground capitalize">
              {key?.replace(/([A-Z])/g, ' $1')?.trim()}:
            </span>
            <span className="text-sm text-foreground font-mono break-all text-right max-w-xs">
              {value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="h-full overflow-y-auto bg-background">
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="text-center mb-6">
          <Icon name="Monitor" size={48} className="text-primary mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-foreground mb-2">System Information</h1>
          <p className="text-muted-foreground">Detailed information about your system and browser environment</p>
        </div>

        {/* System Info Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <InfoSection
            title="System"
            icon="Monitor"
            data={systemInfo?.system}
          />
          
          <InfoSection
            title="Hardware"
            icon="Cpu"
            data={systemInfo?.hardware}
          />
          
          <InfoSection
            title="Browser"
            icon="Globe"
            data={systemInfo?.browser}
          />
          
          <InfoSection
            title="Display"
            icon="Screen"
            data={systemInfo?.display}
          />
          
          <InfoSection
            title="Network"
            icon="Wifi"
            data={systemInfo?.network}
          />
          
          <InfoSection
            title="Performance"
            icon="Activity"
            data={systemInfo?.performance}
          />
        </div>

        {/* Footer */}
        <div className="text-center pt-6 border-t border-border">
          <p className="text-xs text-muted-foreground">
            System information collected on {new Date()?.toLocaleString()}
          </p>
        </div>
      </div>
    </div>
  );
};

export default SystemInfoApplication;