import React, { useState, useEffect, useCallback } from 'react';
import { Helmet } from 'react-helmet';
import SystemInfoHeader from './components/SystemInfoHeader';
import SystemInfoSection from './components/SystemInfoSection';
import SystemInfoGrid from './components/SystemInfoGrid';
import LoadingSkeleton from './components/LoadingSkeleton';
import ErrorDisplay from './components/ErrorDisplay';

const SystemInfoApplicationWindow = () => {
  const [systemData, setSystemData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(new Date());

  // Mock system data - simulating API response
  const mockSystemData = {
    system: {
      hostname: "WebOS-Desktop-2025",
      platform: "Web Browser",
      architecture: "x64",
      osVersion: "WebOS 1.0.0",
      kernelVersion: "5.15.0-web",
      uptime: 86400,
      bootTime: "2025-01-31T12:35:16.805Z"
    },
    hardware: {
      cpu: "Intel Core i7-12700K @ 3.60GHz",
      cores: 12,
      threads: 20,
      memory: {
        total: 17179869184,
        available: 8589934592,
        used: 8589934592,
        usage: 50.0
      },
      storage: {
        total: 1099511627776,
        available: 549755813888,
        used: 549755813888,
        usage: 50.0
      }
    },
    network: {
      hostname: "webos-desktop.local",
      ipAddress: "192.168.1.100",
      macAddress: "00:1B:44:11:3A:B7",
      gateway: "192.168.1.1",
      dns: ["8.8.8.8", "8.8.4.4"],
      connectionType: "Ethernet"
    },
    software: {
      browser: "Chrome 120.0.6099.109",
      userAgent: navigator.userAgent,
      language: "en-US",
      timezone: Intl.DateTimeFormat()?.resolvedOptions()?.timeZone,
      screenResolution: `${screen.width}x${screen.height}`,
      colorDepth: screen.colorDepth
    },
    performance: {
      cpuUsage: 25.5,
      memoryUsage: 50.0,
      diskUsage: 50.0,
      networkLatency: 12,
      processCount: 156,
      threadCount: 892
    }
  };

  const fetchSystemInfo = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // In a real application, this would be:
      // const response = await fetch('/api/system/info');
      // const data = await response.json();
      
      setSystemData(mockSystemData);
      setLastUpdated(new Date());
    } catch (err) {
      setError(err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSystemInfo();
  }, [fetchSystemInfo]);

  // Handle window focus to refresh data
  useEffect(() => {
    const handleFocus = () => {
      if (document.hasFocus() && systemData) {
        fetchSystemInfo();
      }
    };

    window.addEventListener('focus', handleFocus);
    return () => window.removeEventListener('focus', handleFocus);
  }, [fetchSystemInfo, systemData]);

  const handleRefresh = () => {
    fetchSystemInfo();
  };

  const handleRetry = () => {
    fetchSystemInfo();
  };

  if (error) {
    return (
      <>
        <Helmet>
          <title>System Info - Error | WebOS Desktop</title>
        </Helmet>
        <div className="h-full bg-background text-foreground p-6">
          <ErrorDisplay error={error} onRetry={handleRetry} />
        </div>
      </>
    );
  }

  if (isLoading) {
    return (
      <>
        <Helmet>
          <title>System Info - Loading | WebOS Desktop</title>
        </Helmet>
        <div className="h-full bg-background text-foreground p-6 overflow-y-auto">
          <LoadingSkeleton />
        </div>
      </>
    );
  }

  const systemInfo = [
    { label: "Hostname", value: systemData?.system?.hostname, copyable: true },
    { label: "Platform", value: systemData?.system?.platform },
    { label: "Architecture", value: systemData?.system?.architecture },
    { label: "OS Version", value: systemData?.system?.osVersion },
    { label: "Kernel Version", value: systemData?.system?.kernelVersion },
    { label: "Uptime", value: systemData?.system?.uptime, type: "uptime" },
    { label: "Boot Time", value: systemData?.system?.bootTime, type: "date" }
  ];

  const hardwareInfo = [
    { label: "CPU", value: systemData?.hardware?.cpu, copyable: true },
    { label: "CPU Cores", value: systemData?.hardware?.cores },
    { label: "CPU Threads", value: systemData?.hardware?.threads },
    { label: "Total Memory", value: systemData?.hardware?.memory?.total, type: "bytes" },
    { label: "Available Memory", value: systemData?.hardware?.memory?.available, type: "bytes" },
    { label: "Used Memory", value: systemData?.hardware?.memory?.used, type: "bytes" },
    { label: "Memory Usage", value: systemData?.hardware?.memory?.usage, type: "percentage" },
    { label: "Total Storage", value: systemData?.hardware?.storage?.total, type: "bytes" },
    { label: "Available Storage", value: systemData?.hardware?.storage?.available, type: "bytes" },
    { label: "Used Storage", value: systemData?.hardware?.storage?.used, type: "bytes" },
    { label: "Storage Usage", value: systemData?.hardware?.storage?.usage, type: "percentage" }
  ];

  const networkInfo = [
    { label: "Hostname", value: systemData?.network?.hostname, copyable: true },
    { label: "IP Address", value: systemData?.network?.ipAddress, copyable: true },
    { label: "MAC Address", value: systemData?.network?.macAddress, copyable: true },
    { label: "Gateway", value: systemData?.network?.gateway, copyable: true },
    { label: "DNS Servers", value: systemData?.network?.dns?.join(", "), copyable: true },
    { label: "Connection Type", value: systemData?.network?.connectionType }
  ];

  const softwareInfo = [
    { label: "Browser", value: systemData?.software?.browser },
    { label: "User Agent", value: systemData?.software?.userAgent, copyable: true },
    { label: "Language", value: systemData?.software?.language },
    { label: "Timezone", value: systemData?.software?.timezone },
    { label: "Screen Resolution", value: systemData?.software?.screenResolution },
    { label: "Color Depth", value: `${systemData?.software?.colorDepth}-bit` }
  ];

  const performanceInfo = [
    { label: "CPU Usage", value: systemData?.performance?.cpuUsage, type: "percentage" },
    { label: "Memory Usage", value: systemData?.performance?.memoryUsage, type: "percentage" },
    { label: "Disk Usage", value: systemData?.performance?.diskUsage, type: "percentage" },
    { label: "Network Latency", value: `${systemData?.performance?.networkLatency}ms` },
    { label: "Process Count", value: systemData?.performance?.processCount },
    { label: "Thread Count", value: systemData?.performance?.threadCount }
  ];

  return (
    <>
      <Helmet>
        <title>System Information | WebOS Desktop</title>
        <meta name="description" content="View comprehensive system information including hardware specs, software details, and performance metrics" />
      </Helmet>
      
      <div className="h-full bg-background text-foreground p-6 overflow-y-auto">
        <SystemInfoHeader 
          onRefresh={handleRefresh}
          isLoading={isLoading}
          lastUpdated={lastUpdated}
        />

        <div className="space-y-6">
          <SystemInfoSection title="System Information" icon="Monitor">
            <SystemInfoGrid data={systemInfo} columns={2} />
          </SystemInfoSection>

          <SystemInfoSection title="Hardware Information" icon="Cpu">
            <SystemInfoGrid data={hardwareInfo} columns={2} />
          </SystemInfoSection>

          <SystemInfoSection title="Network Information" icon="Wifi">
            <SystemInfoGrid data={networkInfo} columns={2} />
          </SystemInfoSection>

          <SystemInfoSection title="Software Information" icon="Code">
            <SystemInfoGrid data={softwareInfo} columns={1} />
          </SystemInfoSection>

          <SystemInfoSection title="Performance Metrics" icon="Activity" isCollapsible>
            <SystemInfoGrid data={performanceInfo} columns={2} />
          </SystemInfoSection>
        </div>

        {/* Footer */}
        <div className="mt-8 pt-4 border-t border-border text-center">
          <p className="text-xs text-muted-foreground">
            System information refreshed automatically when window gains focus
          </p>
        </div>
      </div>
    </>
  );
};

export default SystemInfoApplicationWindow;