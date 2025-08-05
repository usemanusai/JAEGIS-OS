// Agent Coordination App
import React from 'react';
import AgentCoordinationDashboard from '../../components/ui/AgentCoordinationDashboard';

const AgentCoordinationApp = ({ appId, appName, communication, state, permissions }) => {
  return (
    <div className="w-full h-full bg-gray-900">
      <AgentCoordinationDashboard />
    </div>
  );
};

export default AgentCoordinationApp;
