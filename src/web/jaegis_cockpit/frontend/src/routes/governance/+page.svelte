<script>
    import { onMount } from 'svelte';
    import { API_UTILS, API_CONFIG } from '$lib/config.js';

    let agents = [];
    let activeAgents = [];
    let agentTiers = {};
    let error = null;
    let loading = true;

    async function fetchRealAgentData() {
        try {
            // Fetch all agents using centralized config
            const agentsResponse = await API_UTILS.fetchWithRetry(
                API_UTILS.getApiUrl(API_CONFIG.ENDPOINTS.AGENTS)
            );
            const agentsData = await agentsResponse.json();
            agents = agentsData.agents || [];

            // Fetch active agents using centralized config
            const activeResponse = await API_UTILS.fetchWithRetry(
                API_UTILS.getApiUrl(API_CONFIG.ENDPOINTS.AGENTS_ACTIVE)
            );
            const activeData = await activeResponse.json();
            activeAgents = activeData.active_agents || [];

            // Fetch agent tiers using centralized config
            const tiersResponse = await API_UTILS.fetchWithRetry(
                API_UTILS.getApiUrl(API_CONFIG.ENDPOINTS.AGENTS_TIERS)
            );
            const tiersData = await tiersResponse.json();
            agentTiers = tiersData.tiers || {};

            loading = false;
        } catch (e) {
            error = e.message;
            loading = false;
            console.error("❌ Failed to fetch agent data:", e);
        }
    }

    onMount(fetchRealAgentData);

    function getAgentStatusColor(status) {
        switch (status?.toLowerCase()) {
            case 'active': return 'text-green-400';
            case 'ready': return 'text-blue-400';
            case 'busy': return 'text-yellow-400';
            case 'idle': return 'text-gray-400';
            default: return 'text-gray-400';
        }
    }

    function getTierColor(tier) {
        switch (tier?.toLowerCase()) {
            case 'tier_0': return 'text-purple-400';
            case 'tier_1': return 'text-blue-400';
            case 'tier_2': return 'text-green-400';
            case 'tier_3': return 'text-yellow-400';
            default: return 'text-gray-400';
        }
    }
</script>

<div class="p-8 max-w-7xl mx-auto">
    <h1 class="text-3xl font-bold text-white mb-6">JAEGIS Agent System</h1>
    <p class="text-gray-400 mb-8">Live monitoring of JAEGIS agent hierarchy, coordination, and real-time activity across all tiers.</p>

    {#if loading}
        <div class="text-center p-8">
            <p class="text-gray-400">Loading agent system data...</p>
        </div>
    {:else if error}
        <div class="bg-red-900 border border-red-500 text-red-200 p-4 rounded-lg mb-6">
            <p><strong>Error:</strong> Failed to load agent system data.</p>
            <p class="font-mono mt-2">{error}</p>
        </div>
    {:else}
        <!-- Agent Tiers Overview -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold text-white mb-4">Agent Tiers Overview</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {#each Object.entries(agentTiers.tier_details || {}) as [tierName, tierData]}
                    <div class="bg-gray-800 rounded-lg p-4">
                        <h3 class="text-lg font-bold {getTierColor(tierName)} mb-2">{tierData.name || tierName}</h3>
                        <div class="space-y-2 text-sm">
                            <div class="flex justify-between">
                                <span class="text-gray-400">Total:</span>
                                <span class="text-white">{tierData.count || 0}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-400">Active:</span>
                                <span class="text-green-400">{tierData.active || 0}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-400">Ready:</span>
                                <span class="text-blue-400">{tierData.ready || 0}</span>
                            </div>
                            {#if tierData.description}
                                <p class="text-gray-500 text-xs mt-2">{tierData.description}</p>
                            {/if}
                        </div>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Active Agents -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold text-white mb-4">Active Agents ({activeAgents.length})</h2>
            {#if activeAgents.length === 0}
                <div class="bg-gray-800 rounded-lg p-6 text-center">
                    <p class="text-gray-400">No agents currently active.</p>
                    <p class="text-gray-500 text-sm mt-2">Active agents will appear here when processing tasks.</p>
                </div>
            {:else}
                <div class="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
                    <table class="w-full text-left text-sm text-gray-300">
                        <thead class="bg-gray-900 text-xs text-gray-400 uppercase">
                            <tr>
                                <th class="p-4">Agent ID</th>
                                <th class="p-4">Name</th>
                                <th class="p-4">Tier</th>
                                <th class="p-4">Status</th>
                                <th class="p-4">Performance</th>
                                <th class="p-4">Last Activity</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each activeAgents as agent (agent.agent_id)}
                                <tr class="border-t border-gray-700 hover:bg-gray-700/50">
                                    <td class="p-4 font-mono text-cyan-400">{agent.agent_id}</td>
                                    <td class="p-4">{agent.name}</td>
                                    <td class="p-4 {getTierColor(agent.tier)}">{agent.tier}</td>
                                    <td class="p-4 font-bold {getAgentStatusColor(agent.status)}">{agent.status}</td>
                                    <td class="p-4">{(agent.performance_score * 100).toFixed(1)}%</td>
                                    <td class="p-4">{new Date(agent.last_activity).toLocaleString()}</td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </div>

        <!-- All Agents -->
        <div>
            <h2 class="text-2xl font-bold text-white mb-4">All Registered Agents ({agents.length})</h2>
            {#if agents.length === 0}
                <div class="bg-gray-800 rounded-lg p-6 text-center">
                    <p class="text-gray-400">No agents registered in the system.</p>
                </div>
            {:else}
                <div class="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
                    <table class="w-full text-left text-sm text-gray-300">
                        <thead class="bg-gray-900 text-xs text-gray-400 uppercase">
                            <tr>
                                <th class="p-4">Agent ID</th>
                                <th class="p-4">Name</th>
                                <th class="p-4">Tier</th>
                                <th class="p-4">Status</th>
                                <th class="p-4">Capabilities</th>
                                <th class="p-4">Created</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each agents as agent (agent.agent_id)}
                                <tr class="border-t border-gray-700 hover:bg-gray-700/50">
                                    <td class="p-4 font-mono text-cyan-400">{agent.agent_id}</td>
                                    <td class="p-4">{agent.name}</td>
                                    <td class="p-4 {getTierColor(agent.tier)}">{agent.tier}</td>
                                    <td class="p-4 font-bold {getAgentStatusColor(agent.status)}">{agent.status}</td>
                                    <td class="p-4">{agent.capabilities?.length || 0} capabilities</td>
                                    <td class="p-4">{new Date(agent.created_at).toLocaleString()}</td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </div>
    {/if}
</div>
