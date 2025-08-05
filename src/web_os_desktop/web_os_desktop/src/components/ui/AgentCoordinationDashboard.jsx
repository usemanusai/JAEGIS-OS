// AgentCoordinationDashboard.jsx - Agent Coordination Visualization
import React, { useState, useEffect } from 'react';
import { useASCEND, useCoreServices } from '../../hooks/useCoreServices';

const AgentCoordinationDashboard = () => {
  const [agentHierarchy, setAgentHierarchy] = useState([]);
  const [activeTasks, setActiveTasks] = useState([]);
  const [selectedTier, setSelectedTier] = useState(null);
  const [agentMetrics, setAgentMetrics] = useState({});
  const [communicationFlow, setCommunicationFlow] = useState([]);
  
  const { service: ascendService, isHealthy: ascendHealthy } = useASCEND();
  const { serviceStatuses } = useCoreServices();
  
  useEffect(() => {
    initializeAgentData();
    const interval = setInterval(updateAgentData, 5000); // Update every 5 seconds
    return () => clearInterval(interval);
  }, []);
  
  // Initialize agent hierarchy data
  const initializeAgentData = () => {
    const hierarchy = [
      {
        tier: 0,
        name: 'N.L.D.S.',
        description: 'Natural Language Data Science - Tier 0 Command Center',
        agents: [
          { id: 'nlds_primary', name: 'N.L.D.S. Primary', status: 'active', load: 45 }
        ],
        color: 'bg-purple-600'
      },
      {
        tier: 1,
        name: 'Core Services',
        description: 'Primary JAEGIS Services - Tier 1',
        agents: [
          { id: 'script', name: 'S.C.R.I.P.T.', status: 'active', load: 32 },
          { id: 'atlas', name: 'A.T.L.A.S.', status: 'active', load: 28 },
          { id: 'helm', name: 'H.E.L.M.', status: 'active', load: 41 },
          { id: 'mastr', name: 'M.A.S.T.R.', status: 'active', load: 35 },
          { id: 'ascend', name: 'A.S.C.E.N.D.', status: 'active', load: 39 },
          { id: 'cori', name: 'C.O.R.I.', status: 'active', load: 22 }
        ],
        color: 'bg-blue-600'
      },
      {
        tier: 2,
        name: 'System Agents',
        description: 'Specialized System Management - Tier 2',
        agents: [
          { id: 'talent_scout', name: 'Talent Scout', status: 'active', load: 15 },
          { id: 'squad_architect', name: 'Squad Architect', status: 'active', load: 18 },
          { id: 'synthesizer', name: 'Synthesizer', status: 'active', load: 25 },
          { id: 'drill_instructor', name: 'Drill Instructor', status: 'active', load: 12 }
        ],
        color: 'bg-green-600'
      },
      {
        tier: 3,
        name: 'Application Agents',
        description: 'Application-Specific Agents - Tier 3',
        agents: [
          { id: 'app_manager', name: 'App Manager', status: 'active', load: 20 },
          { id: 'ui_controller', name: 'UI Controller', status: 'active', load: 16 },
          { id: 'data_processor', name: 'Data Processor', status: 'active', load: 30 }
        ],
        color: 'bg-yellow-600'
      },
      {
        tier: 4,
        name: 'Task Agents',
        description: 'Task Execution and Workflow - Tier 4',
        agents: [
          { id: 'task_executor', name: 'Task Executor', status: 'active', load: 45 },
          { id: 'workflow_manager', name: 'Workflow Manager', status: 'active', load: 33 },
          { id: 'scheduler', name: 'Scheduler', status: 'active', load: 28 }
        ],
        color: 'bg-orange-600'
      },
      {
        tier: 5,
        name: 'Utility Agents',
        description: 'Support and Utility Functions - Tier 5',
        agents: [
          { id: 'logger', name: 'Logger', status: 'active', load: 8 },
          { id: 'monitor', name: 'Monitor', status: 'active', load: 12 },
          { id: 'validator', name: 'Validator', status: 'active', load: 15 }
        ],
        color: 'bg-red-600'
      },
      {
        tier: 6,
        name: 'Specialized Agents',
        description: 'Domain-Specific Agents - Tier 6',
        agents: [
          { id: 'research_agent', name: 'Research Agent', status: 'active', load: 22 },
          { id: 'analysis_agent', name: 'Analysis Agent', status: 'active', load: 18 },
          { id: 'communication_agent', name: 'Communication Agent', status: 'active', load: 14 }
        ],
        color: 'bg-indigo-600'
      }
    ];
    
    setAgentHierarchy(hierarchy);
    
    // Initialize active tasks
    setActiveTasks([
      { id: 1, title: 'Data Processing Pipeline', assignedTo: 'data_processor', progress: 75, priority: 'high' },
      { id: 2, title: 'UI Component Rendering', assignedTo: 'ui_controller', progress: 45, priority: 'medium' },
      { id: 3, title: 'System Health Check', assignedTo: 'monitor', progress: 90, priority: 'low' },
      { id: 4, title: 'Agent Synthesis', assignedTo: 'synthesizer', progress: 30, priority: 'high' }
    ]);
  };
  
  // Update agent data
  const updateAgentData = async () => {
    if (ascendHealthy && ascendService) {
      try {
        const lifecycleStatus = await ascendService.getAgentLifecycleStatus();
        // Update agent statuses based on real data
        console.log('Agent lifecycle status:', lifecycleStatus);
      } catch (error) {
        console.error('Failed to fetch agent status:', error);
      }
    }
    
    // Simulate real-time updates
    setAgentHierarchy(prev => prev.map(tier => ({
      ...tier,
      agents: tier.agents.map(agent => ({
        ...agent,
        load: Math.max(5, Math.min(95, agent.load + (Math.random() - 0.5) * 10))
      }))
    })));
  };
  
  // Get status color
  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'idle': return 'bg-yellow-500';
      case 'error': return 'bg-red-500';
      case 'offline': return 'bg-gray-500';
      default: return 'bg-gray-500';
    }
  };
  
  // Get load color
  const getLoadColor = (load) => {
    if (load < 30) return 'bg-green-500';
    if (load < 70) return 'bg-yellow-500';
    return 'bg-red-500';
  };
  
  // Get priority color
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'text-red-400';
      case 'medium': return 'text-yellow-400';
      case 'low': return 'text-green-400';
      default: return 'text-gray-400';
    }
  };
  
  return (
    <div className="p-6 bg-gray-900 text-white min-h-screen">
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-2">Agent Coordination Dashboard</h1>
        <p className="text-gray-400">Real-time visualization of 7-tier agent hierarchy and task coordination</p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent Hierarchy */}
        <div className="lg:col-span-2">
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Agent Hierarchy (7 Tiers)</h2>
            <div className="space-y-4">
              {agentHierarchy.map((tier) => (
                <div key={tier.tier} className="border border-gray-700 rounded-lg p-4">
                  <div 
                    className="flex items-center justify-between cursor-pointer"
                    onClick={() => setSelectedTier(selectedTier === tier.tier ? null : tier.tier)}
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`w-4 h-4 rounded ${tier.color}`}></div>
                      <div>
                        <h3 className="font-medium">Tier {tier.tier}: {tier.name}</h3>
                        <p className="text-sm text-gray-400">{tier.description}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-400">{tier.agents.length} agents</span>
                      <svg 
                        className={`w-5 h-5 transform transition-transform ${selectedTier === tier.tier ? 'rotate-180' : ''}`}
                        fill="none" 
                        stroke="currentColor" 
                        viewBox="0 0 24 24"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                  </div>
                  
                  {selectedTier === tier.tier && (
                    <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
                      {tier.agents.map((agent) => (
                        <div key={agent.id} className="bg-gray-700 rounded p-3">
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-medium">{agent.name}</span>
                            <div className={`w-3 h-3 rounded-full ${getStatusColor(agent.status)}`}></div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="text-xs text-gray-400">Load:</span>
                            <div className="flex-1 bg-gray-600 rounded-full h-2">
                              <div 
                                className={`h-2 rounded-full ${getLoadColor(agent.load)}`}
                                style={{ width: `${agent.load}%` }}
                              ></div>
                            </div>
                            <span className="text-xs text-gray-400">{Math.round(agent.load)}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Active Tasks and Metrics */}
        <div className="space-y-6">
          {/* Active Tasks */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Active Tasks</h2>
            <div className="space-y-3">
              {activeTasks.map((task) => (
                <div key={task.id} className="bg-gray-700 rounded p-3">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-sm">{task.title}</span>
                    <span className={`text-xs ${getPriorityColor(task.priority)}`}>
                      {task.priority}
                    </span>
                  </div>
                  <div className="text-xs text-gray-400 mb-2">
                    Assigned to: {task.assignedTo}
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-600 rounded-full h-2">
                      <div 
                        className="h-2 bg-blue-500 rounded-full"
                        style={{ width: `${task.progress}%` }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-400">{task.progress}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* System Metrics */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">System Metrics</h2>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Total Agents</span>
                  <span>{agentHierarchy.reduce((sum, tier) => sum + tier.agents.length, 0)}</span>
                </div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Active Agents</span>
                  <span className="text-green-400">
                    {agentHierarchy.reduce((sum, tier) => 
                      sum + tier.agents.filter(a => a.status === 'active').length, 0
                    )}
                  </span>
                </div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Average Load</span>
                  <span>
                    {Math.round(
                      agentHierarchy.reduce((sum, tier) => 
                        sum + tier.agents.reduce((tierSum, agent) => tierSum + agent.load, 0), 0
                      ) / agentHierarchy.reduce((sum, tier) => sum + tier.agents.length, 0)
                    )}%
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Active Tasks</span>
                  <span>{activeTasks.length}</span>
                </div>
              </div>
            </div>
          </div>
          
          {/* Core Services Status */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Core Services</h2>
            <div className="space-y-2">
              {serviceStatuses.map((service) => (
                <div key={service.service} className="flex items-center justify-between">
                  <span className="text-sm">{service.service}</span>
                  <div className={`w-3 h-3 rounded-full ${getStatusColor(service.status)}`}></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentCoordinationDashboard;
