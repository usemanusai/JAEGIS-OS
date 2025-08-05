<script>
  import { Users, Bot, Zap } from 'lucide-svelte';
  import { onMount } from 'svelte';

  export let agentCount;

  let agentTypes = [];
  let loading = true;
  let error = null;

  // Import configuration
  import { API_UTILS, API_CONFIG } from '$lib/config.js';

  // Fetch real agent data from API using centralized config
  async function fetchAgentTypes() {
    try {
      const response = await API_UTILS.fetchWithRetry(
        API_UTILS.getApiUrl(API_CONFIG.ENDPOINTS.AGENTS_TIERS)
      );
      const data = await response.json();

      // Transform real tier data into component format
      agentTypes = Object.entries(data.tiers?.tier_details || {}).map(([tierName, tierData]) => ({
        name: tierData.name || tierName,
        count: tierData.count || 0,
        status: tierData.active > 0 ? 'active' : 'idle',
        type: tierName.toLowerCase().includes('tier_0') ? 'system' :
              tierName.toLowerCase().includes('tier_1') ? 'cognitive' :
              tierName.toLowerCase().includes('tier_2') ? 'tool' : 'forge'
      }));

      loading = false;
    } catch (e) {
      error = e.message;
      loading = false;
      console.error("Failed to fetch agent types:", e);

      // Fallback to basic structure if API fails
      agentTypes = [
        { name: 'JAEGIS Agents', count: agentCount || 0, status: 'unknown', type: 'system' }
      ];
    }
  }

  onMount(fetchAgentTypes);
  
  function getAgentTypeIcon(type) {
    switch (type) {
      case 'system': return Zap;
      case 'tool': return Bot;
      case 'forge': return Users;
      case 'cognitive': return Users;
      default: return Bot;
    }
  }
  
  function getAgentTypeColor(type) {
    switch (type) {
      case 'system': return 'text-purple-600 bg-purple-100';
      case 'tool': return 'text-blue-600 bg-blue-100';
      case 'forge': return 'text-green-600 bg-green-100';
      case 'cognitive': return 'text-orange-600 bg-orange-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  }
  
  function getStatusColor(status) {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100';
      case 'idle': return 'text-yellow-600 bg-yellow-100';
      case 'error': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  }
</script>

<div class="card">
  <div class="card-header">
    <div class="flex items-center">
      <Users class="h-5 w-5 text-jaegis-primary mr-2" />
      <h3 class="card-title">Active Agents</h3>
    </div>
    <div class="text-right">
      <div class="text-2xl font-bold text-gray-900">{agentCount}</div>
      <div class="text-sm text-gray-500">Total Active</div>
    </div>
  </div>
  
  <div class="space-y-4">
    {#if loading}
      <div class="text-center p-4">
        <p class="text-gray-500">Loading agent data...</p>
      </div>
    {:else if error}
      <div class="text-center p-4">
        <p class="text-red-500 text-sm">Error: {error}</p>
        <p class="text-gray-500 text-xs mt-1">Using fallback data</p>
      </div>
    {/if}

    <!-- Agent breakdown -->
    <div class="space-y-3">
      {#each agentTypes as agent}
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div class="flex items-center">
            <div class="w-8 h-8 rounded-md flex items-center justify-center {getAgentTypeColor(agent.type)}">
              <svelte:component this={getAgentTypeIcon(agent.type)} class="h-4 w-4" />
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-900">{agent.name}</p>
              <p class="text-xs text-gray-500 capitalize">{agent.type} agent</p>
            </div>
          </div>

          <div class="flex items-center space-x-3">
            <span class="text-sm font-medium text-gray-900">{agent.count}</span>
            <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium {getStatusColor(agent.status)}">
              {agent.status}
            </span>
          </div>
        </div>
      {/each}
    </div>
    
    <!-- Quick stats -->
    <div class="border-t border-gray-200 pt-4">
      <div class="grid grid-cols-3 gap-4 text-center">
        <div>
          <div class="text-lg font-semibold text-gray-900">
            {agentTypes.filter(a => a.status === 'active').length}
          </div>
          <div class="text-xs text-gray-500">Active Types</div>
        </div>
        <div>
          <div class="text-lg font-semibold text-gray-900">
            {agentTypes.reduce((sum, a) => sum + a.count, 0)}
          </div>
          <div class="text-xs text-gray-500">Total Agents</div>
        </div>
        <div>
          <div class="text-lg font-semibold text-green-600">
            100%
          </div>
          <div class="text-xs text-gray-500">Uptime</div>
        </div>
      </div>
    </div>
  </div>
</div>
