// Monitoring Dashboard App
import React from 'react';
import RealTimeMonitoringDashboard from '../../components/ui/RealTimeMonitoringDashboard';

const MonitoringDashboardApp = ({ appId, appName, communication, state, permissions }) => {
  return (
    <div className="w-full h-full bg-gray-900">
      <RealTimeMonitoringDashboard />
    </div>
  );
};

export default MonitoringDashboardApp;
